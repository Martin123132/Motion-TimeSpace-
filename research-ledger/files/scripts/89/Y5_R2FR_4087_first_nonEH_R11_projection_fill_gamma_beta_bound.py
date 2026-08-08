from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4087-Y5-R2FR-first-nonEH-R11-projection-fill-gamma-beta-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "FIRST_R11_R2_SCALAR_MODE_BOUND_FILLED_GAMMA_EXACT_BETA_ASYMPTOTIC_LOCAL_GR_STILL_NONCLAIM"

R_SUN_M = 6.957e8
AU_M = 149_597_870_700.0
CASSINI_IMPACT_RSUN = 1.6
GAMMA_BOUND = 2.3e-5
BETA_BOUND = 8.0e-5
SCALAR_COUPLING_A = 1.0 / 3.0
HBAR_C_EV_M = 1.973269804e-7
EULER_GAMMA = 0.5772156649015329


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4087_00_4086_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_NEXT_TARGET.csv",
        "4087-Y5-R2FR-first-nonEH-R11-projection-fill-gamma-beta-bound.md",
        "4086 selects the first non-EH/R11 gamma-beta projection fill.",
    ),
    "SRC4087_01_4086_projection_formulas": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_NONEH_PPN_PROJECTION_FORMULAS.csv",
        "PROJ4086_1_gamma",
        "4086 gives the gamma/beta projection interfaces for non-EH residuals.",
    ),
    "SRC4087_02_4086_family_route": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_R11_FAMILY_TO_PPN_ROUTE.csv",
        "R2_fR_scalar_mode",
        "4086 marks R2/f(R) scalar mode as the highest-priority first numeric/zero fill.",
    ),
    "SRC4087_03_4085_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_0_gamma_cassini",
        "4085 supplies gamma and beta empirical bounds.",
    ),
    "SRC4087_04_3918_gamma": (
        SOURCE_DIR / "P8_Y5_R2FR_3918_DELTA_GAMMA_R11_THEOREM_AND_BOUND.csv",
        "delta_gamma_R11",
        "3918 provides the tracefree spatial slip projection that gamma scores.",
    ),
    "SRC4087_05_4042_family": (
        SOURCE_DIR / "P8_Y5_R2FR_4042_R11_FAMILY_CLASSIFICATION.csv",
        "R11F4042_01",
        "4042 classifies R2/f(R) scalar mode as a live R11 family unless absent/double-zero/screened.",
    ),
    "SRC4087_06_r11_executable": (
        SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv",
        "R2_fR_scalar_mode",
        "The R11 executable vector schema still lacks a parent numeric/zero coefficient for R2/f(R).",
    ),
}


WEB_SOURCES = [
    {
        "source_id": "WEB4087_0_chiba_smith_erickcek_2006",
        "title": "Solar System constraints to general f(R) gravity",
        "authors": "Takeshi Chiba, Tristan L. Smith, Adrienne L. Erickcek",
        "year": "2006",
        "url": "https://arxiv.org/abs/astro-ph/0611867",
        "source_role": "metric f(R) scalar-tensor equivalence and solar-system gamma danger when the scalar propagates",
        "extracted_result": "metric f(R) is equivalent to scalar-tensor and predicts gamma=1/2 when the scalar propagates over solar-system scales",
        "confidence": "arXiv_peer_literature_preprint",
        "timestamp_utc": TIMESTAMP,
    },
    {
        "source_id": "WEB4087_1_zhu_li_2026_quadratic_ppn",
        "title": "Parameterized post-Newtonian analysis of quadratic gravity and solar system constraints",
        "authors": "Jie Zhu, Hao Li",
        "year": "2026",
        "url": "https://link.springer.com/article/10.1140/epjc/s10052-026-15793-y",
        "source_role": "quadratic-gravity massive scalar/spin-2 PPN potentials, masses and beta asymptotics",
        "extracted_result": "quadratic gravity has scalar mass m_R^2=1/(6 mu), spin-2 mass m_W^2=1/(2 lambda), exponentially suppressed gamma/beta deviations and f(R) limit beta asymptotics",
        "confidence": "open_access_Eur_Phys_J_C_article",
        "timestamp_utc": TIMESTAMP,
    },
    {
        "source_id": "WEB4087_2_iau_nominal_constants",
        "title": "IAU 2015 Resolution B3 nominal solar radius and IAU 2012 AU convention",
        "authors": "International Astronomical Union",
        "year": "2015",
        "url": "https://www.iau.org/common/Uploaded%20files/IAUGA2015-Resolution-B3-recommended-nominal-conversion.pdf",
        "supporting_url": "https://observatoiredeparis.psl.eu/the-new-definition-of-the-astronomical-unit.html",
        "source_role": "unit conversion only",
        "extracted_result": "R_sun^N=6.957e8 m; AU=149597870700 m",
        "confidence": "official_nominal_unit_conventions",
        "timestamp_utc": TIMESTAMP,
    },
]


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def gamma_delta_from_x(x_value: float) -> float:
    y_value = math.exp(-x_value)
    return abs((3.0 - y_value) / (3.0 + y_value) - 1.0)


def beta_delta_from_x_asymptotic(x_value: float) -> float:
    y_value = math.exp(-x_value)
    geff = 1.0 + y_value / 3.0
    geff2_beta_minus_one = (
        (1.0 / 3.0) * x_value * y_value * math.log(2.0 * x_value)
        + ((9.0 * EULER_GAMMA - 4.0) / 27.0) * x_value * y_value
    )
    beta_value = (1.0 + geff2_beta_minus_one) / (geff * geff)
    return abs(beta_value - 1.0)


def solve_x_for_bound(function, target: float, low: float = 1.0e-6, high: float = 200.0) -> float:
    while function(high) > target:
        high *= 2.0
        if high > 1.0e6:
            raise RuntimeError("could not bracket suppression solution")
    for _ in range(160):
        mid = 0.5 * (low + high)
        if function(mid) > target:
            low = mid
        else:
            high = mid
    return high


def derived_values() -> dict:
    impact_rsun = CASSINI_IMPACT_RSUN
    impact_m = impact_rsun * R_SUN_M
    impact_au = impact_m / AU_M

    y_gamma_max = 3.0 * GAMMA_BOUND / (2.0 - GAMMA_BOUND)
    x_gamma_min = -math.log(y_gamma_max)
    lambda_gamma_rsun = impact_rsun / x_gamma_min
    lambda_gamma_m = lambda_gamma_rsun * R_SUN_M
    lambda_gamma_au = lambda_gamma_m / AU_M

    x_beta_min = solve_x_for_bound(beta_delta_from_x_asymptotic, BETA_BOUND)
    lambda_beta_rsun = impact_rsun / x_beta_min
    lambda_beta_m = lambda_beta_rsun * R_SUN_M
    lambda_beta_au = lambda_beta_m / AU_M

    x_combined_min = max(x_gamma_min, x_beta_min)
    lambda_combined_rsun = impact_rsun / x_combined_min
    lambda_combined_m = lambda_combined_rsun * R_SUN_M
    lambda_combined_au = lambda_combined_m / AU_M
    mu_combined_m2 = lambda_combined_m**2 / 6.0
    mu_combined_rsun2 = lambda_combined_rsun**2 / 6.0
    m_inv_au = 1.0 / lambda_combined_au
    m_energy_ev = HBAR_C_EV_M / lambda_combined_m

    return {
        "impact_rsun": impact_rsun,
        "impact_m": impact_m,
        "impact_au": impact_au,
        "y_gamma_max": y_gamma_max,
        "x_gamma_min": x_gamma_min,
        "lambda_gamma_rsun": lambda_gamma_rsun,
        "lambda_gamma_m": lambda_gamma_m,
        "lambda_gamma_au": lambda_gamma_au,
        "x_beta_min": x_beta_min,
        "lambda_beta_rsun": lambda_beta_rsun,
        "lambda_beta_m": lambda_beta_m,
        "lambda_beta_au": lambda_beta_au,
        "x_combined_min": x_combined_min,
        "lambda_combined_rsun": lambda_combined_rsun,
        "lambda_combined_m": lambda_combined_m,
        "lambda_combined_au": lambda_combined_au,
        "mu_combined_m2": mu_combined_m2,
        "mu_combined_rsun2": mu_combined_rsun2,
        "m_inv_au": m_inv_au,
        "m_energy_ev": m_energy_ev,
        "gamma_at_combined": gamma_delta_from_x(x_combined_min),
        "beta_at_combined": beta_delta_from_x_asymptotic(x_combined_min),
    }


VALUES = derived_values()


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    for row in WEB_SOURCES:
        rows.append(
            {
                "source_id": row["source_id"],
                "source_type": "web_literature_or_unit_convention",
                "path_or_url": row["url"],
                "needle": row["extracted_result"],
                "role": row["source_role"],
                "exists": "web_checked",
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4087_07_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for first R11 scalar-mode gamma/beta bound fill.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def derivation_rows() -> List[dict]:
    return [
        {
            "row_id": "R2F4087_0_mode_selection",
            "piece": "first live R11 family selected",
            "statement": "Select the R2/f(R) scalar mode because 4086 marks it as the highest-priority gamma/beta/range family and it has a known scalar Yukawa map.",
            "formula": "f(R)=R+mu R^2 subset; m_R^2=1/(6 mu); y=exp(-m_R b)",
            "derived_result": "R2_SCALAR_MODE_SELECTED_FOR_FIRST_BOUND_FILL",
            "status": "EXECUTABLE_NONCLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "R2F4087_1_gamma_formula",
            "piece": "gamma projection",
            "statement": "For the scalar-only f(R) limit with standard 1/3 scalar Yukawa strength, the first-PN metric potentials give gamma(b)=(3-y)/(3+y).",
            "formula": "gamma_R2(b)=(3-exp(-b/lambda_R))/(3+exp(-b/lambda_R)); |gamma-1|=2y/(3+y)",
            "derived_result": "EXACT_SCALAR_YUKAWA_GAMMA_BOUND_FORMULA",
            "status": "DERIVED_FOR_STANDARD_METRIC_FR_NORMALIZATION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "R2F4087_2_gamma_suppression_condition",
            "piece": "Cassini gamma condition",
            "statement": "Imposing the 4085 Cassini bound B_gamma yields y <= 3 B_gamma/(2-B_gamma), so b/lambda_R must exceed log((2-B_gamma)/(3B_gamma)).",
            "formula": "exp(-b/lambda_R) <= 3B_gamma/(2-B_gamma)",
            "derived_result": "EXACT_CASSINI_GAMMA_SUPPRESSION_INEQUALITY",
            "status": "NUMERIC_BOUND_FILLED",
            "numeric_value": f"{VALUES['x_gamma_min']:.12e}",
            "units": "minimum_b_over_lambda_from_gamma",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "R2F4087_3_beta_asymptotic_formula",
            "piece": "beta projection",
            "statement": "Using the f(R) limit of the quadratic-gravity 2PN result, the effective beta deviation is exponentially suppressed but includes x exp(-x) log(2x) terms.",
            "formula": "G_eff^2 beta - 1 ~= (1/3)x e^-x ln(2x)+((9 gamma_E-4)/27)x e^-x; G_eff=1+e^-x/3",
            "derived_result": "ASYMPTOTIC_R2_SCALAR_BETA_BOUND_FORMULA",
            "status": "ASYMPTOTIC_NUMERIC_BOUND_FILLED",
            "numeric_value": f"{VALUES['x_beta_min']:.12e}",
            "units": "minimum_b_over_lambda_from_beta_asymptotic",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "R2F4087_4_combined_condition",
            "piece": "combined local PPN condition",
            "statement": "The scalar R2/f(R) branch survives the 4085 gamma/beta gate only if x=b/lambda_R is at least the stricter of the gamma and beta suppression thresholds, or if the parent proves absence/double-zero.",
            "formula": "x >= max(x_gamma_min,x_beta_min)",
            "derived_result": "COMBINED_R2_SCALAR_LOCAL_PPN_BOUND",
            "status": "NUMERIC_BOUND_FILLED_NONCLAIM",
            "numeric_value": f"{VALUES['x_combined_min']:.12e}",
            "units": "minimum_b_over_lambda",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            "bound_id": "B4087_0_gamma_yukawa_amplitude",
            "mode": "R2_fR_scalar_mode",
            "observable": "gamma_minus_1",
            "bound_input": f"{GAMMA_BOUND:.12e}",
            "bound_input_units": "dimensionless",
            "derived_condition": "exp(-b/lambda_R) <= 3B_gamma/(2-B_gamma)",
            "numeric_value": f"{VALUES['y_gamma_max']:.12e}",
            "numeric_units": "max_yukawa_factor_y",
            "source": "4085 Cassini gamma bound plus scalar f(R) gamma formula",
            "status": "EXACT_STANDARD_FR_GAMMA_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4087_1_gamma_range",
            "mode": "R2_fR_scalar_mode",
            "observable": "lambda_R_gamma_only",
            "bound_input": f"{VALUES['impact_rsun']:.12e}",
            "bound_input_units": "solar_radii Cassini impact parameter",
            "derived_condition": "lambda_R <= b/x_gamma_min",
            "numeric_value": f"{VALUES['lambda_gamma_rsun']:.12e}",
            "numeric_units": "solar_radii",
            "numeric_value_m": f"{VALUES['lambda_gamma_m']:.12e}",
            "numeric_value_au": f"{VALUES['lambda_gamma_au']:.12e}",
            "status": "GAMMA_ONLY_RANGE_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4087_2_beta_range_asymptotic",
            "mode": "R2_fR_scalar_mode",
            "observable": "lambda_R_beta_asymptotic",
            "bound_input": f"{BETA_BOUND:.12e}",
            "bound_input_units": "dimensionless",
            "derived_condition": "abs(beta_R2_asymptotic(x)-1) <= B_beta",
            "numeric_value": f"{VALUES['lambda_beta_rsun']:.12e}",
            "numeric_units": "solar_radii",
            "numeric_value_m": f"{VALUES['lambda_beta_m']:.12e}",
            "numeric_value_au": f"{VALUES['lambda_beta_au']:.12e}",
            "status": "BETA_ASYMPTOTIC_RANGE_BOUND_NONCLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4087_3_combined_range",
            "mode": "R2_fR_scalar_mode",
            "observable": "lambda_R_combined_gamma_beta",
            "bound_input": "max(gamma threshold,beta asymptotic threshold)",
            "bound_input_units": "componentwise PPN",
            "derived_condition": "lambda_R <= b/max(x_gamma,x_beta)",
            "numeric_value": f"{VALUES['lambda_combined_rsun']:.12e}",
            "numeric_units": "solar_radii",
            "numeric_value_m": f"{VALUES['lambda_combined_m']:.12e}",
            "numeric_value_au": f"{VALUES['lambda_combined_au']:.12e}",
            "status": "STRICTER_BETA_ASYMPTOTIC_BOUND_SELECTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4087_4_mu_coefficient_standard_fr",
            "mode": "R2_fR_scalar_mode",
            "observable": "mu_R2_coefficient",
            "bound_input": "m_R^2=1/(6mu), lambda_R=1/m_R",
            "bound_input_units": "standard metric f(R)=R+mu R^2 normalization",
            "derived_condition": "mu <= lambda_R^2/6",
            "numeric_value": f"{VALUES['mu_combined_m2']:.12e}",
            "numeric_units": "m^2",
            "numeric_value_rsun2": f"{VALUES['mu_combined_rsun2']:.12e}",
            "status": "STANDARD_NORMALIZATION_COEFFICIENT_BOUND_TEMPLATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4087_5_mass_scale",
            "mode": "R2_fR_scalar_mode",
            "observable": "m_R_min",
            "bound_input": "1/lambda_R_combined",
            "bound_input_units": "inverse length",
            "derived_condition": "m_R >= max(x_gamma,x_beta)/b",
            "numeric_value": f"{VALUES['m_inv_au']:.12e}",
            "numeric_units": "AU^-1",
            "numeric_value_energy_ev": f"{VALUES['m_energy_ev']:.12e}",
            "status": "MASS_SCALE_TRANSLATION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def smoke_case_rows() -> List[dict]:
    cases = [
        ("CASE4087_0_massless", 0.0, "massless_or_solar_system_long_range_scalar"),
        ("CASE4087_1_gamma_edge", VALUES["x_gamma_min"], "gamma_bound_edge"),
        ("CASE4087_2_beta_edge", VALUES["x_beta_min"], "beta_bound_edge"),
        ("CASE4087_3_strong_screening", 20.0, "comfortably_short_range"),
    ]
    rows: List[dict] = []
    for case_id, x_value, meaning in cases:
        gamma_delta = gamma_delta_from_x(x_value)
        beta_delta = beta_delta_from_x_asymptotic(x_value) if x_value > 0.0 else float("inf")
        rows.append(
            {
                "case_id": case_id,
                "meaning": meaning,
                "x_b_over_lambda": f"{x_value:.12e}",
                "gamma_delta": f"{gamma_delta:.12e}",
                "gamma_pass": bool_string(gamma_delta <= GAMMA_BOUND),
                "beta_delta_asymptotic": "inf" if math.isinf(beta_delta) else f"{beta_delta:.12e}",
                "beta_pass_asymptotic": bool_string((not math.isinf(beta_delta)) and beta_delta <= BETA_BOUND),
                "overall_pass_for_this_template": bool_string(gamma_delta <= GAMMA_BOUND and (not math.isinf(beta_delta)) and beta_delta <= BETA_BOUND),
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def r11_update_rows() -> List[dict]:
    return [
        {
            "update_id": "R11UP4087_0",
            "operator_family": "R2_fR_scalar_mode",
            "old_status": "HIGH_PRIORITY_FIRST_NUMERIC_OR_ZERO_FILL",
            "new_status": "FILLED_STANDARD_FR_SCALAR_GAMMA_BETA_BOUND_TEMPLATE",
            "zero_or_bound": "bound unless parent proves absent/double-zero",
            "condition_to_pass": f"lambda_R <= {VALUES['lambda_combined_rsun']:.6e} R_sun for standard scalar coupling, or C_i(X0)=dC_i(X0)=0 with mass-gap/readout silence",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "R11UP4087_1",
            "operator_family": "R2_fR_scalar_mode",
            "old_status": "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT",
            "new_status": "NORMALIZATION_TEMPLATE_READY_NOT_PARENT_COEFFICIENT",
            "zero_or_bound": "mu <= lambda_R^2/6 only under standard f(R)=R+mu R^2 normalization",
            "condition_to_pass": "MTS must map its c_R2 normalization to mu before this can become a parent-owned coefficient bound",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4087_0_main",
            "decision": DECISION,
            "meaning": "The first non-EH family is no longer merely missing. If an f(R)-like R2 scalar survives with standard coupling, it must be short-ranged enough to satisfy the gamma/beta bound, or parent-zeroed by the 4086 double-zero mechanism.",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_required_move": "Map MTS c_R2 normalization to the standard mu slot, or move to the Ricci/Weyl spin-2 tracefree projection family.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4087_1_physics_read",
            "decision": "LONG_RANGE_R2_SCALAR_BRANCH_FAILS_LOCAL_GR",
            "meaning": "A massless or solar-system-long-range metric f(R) scalar gives gamma far from one. MTS can keep this route only by absence, double-zero, mass gap/screening, or a different parent normalization that is explicitly mapped.",
            "claim_status": "DISCIPLINE_RULE",
            "next_required_move": "Do not call local GR unless this family is parent-zeroed or bounded.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4087_0_R2_scalar_pass",
            "claim": "MTS R2/f(R) scalar family passes local PPN",
            "allowed": "False",
            "why_not": "4087 gives a standard-normalization bound template, not a parent-owned MTS coefficient or mass-gap derivation.",
            "minimum_unlock": "Map MTS c_R2/mu normalization and prove lambda_R below the combined bound, or prove parent absent/double-zero with readout silence.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4087_1_local_GR",
            "claim": "MTS reduces to local GR",
            "allowed": "False",
            "why_not": "Only one R11 family has been filled; other non-EH/projector/vector/source families remain live.",
            "minimum_unlock": "All 4086 R11 family rows zeroed or bounded, plus source/readout/conservation clauses.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4087_2_forward_progress",
            "claim": "4087 advances the framework",
            "allowed": "True_private_checkpoint",
            "why_not": "This is a private derived/bounded checkpoint, not a public local-GR proof.",
            "minimum_unlock": "N/A",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4087_0",
            "next_target": "4088-Y5-R2FR-map-MTS-cR2-normalization-or-Ricci-Weyl-spin2-slip-bound.md",
            "script": "scripts/Y5_R2FR_4088_map_MTS_cR2_or_Ricci_Weyl_spin2_slip_bound.py",
            "why": "4087 gives a standard f(R) scalar bound. The next best route is either map the actual MTS c_R2 coefficient into this mu slot, or fill the neighbouring Ricci/Weyl spin-2 tracefree slip projection.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4087_1",
            "next_target": "R10_alpha_curve_reuse_for_scalar_range",
            "script": "defer_until_R10_bound_curve_claim_ready",
            "why": "The same scalar mode is also a finite-range alpha(lambda) branch; R10 can later provide a stronger short-range bound if real curve rows are sourced.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4087",
            "status": "private_nonclaim_checkpoint_complete",
            "decision": DECISION,
            "public_claim": "False",
            "github_action": "False",
            "formalization_workbench_modified_by_script": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def validation_rows(output_paths: Iterable[Path]) -> List[dict]:
    paths = list(output_paths)
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        add(
            f"VAL4087_SRC_{source_id}",
            "local source exists and contains needle",
            bool(exists and contains),
            f"{path} | needle={needle} | role={role}",
        )

    for path in paths:
        rows = parse_csv(path)
        add(
            f"VAL4087_CSV_{path.stem}",
            "generated CSV parses and is non-empty",
            bool(rows),
            f"{path} rows={len(rows)}",
        )

    gamma_edge_ok = gamma_delta_from_x(VALUES["x_gamma_min"]) <= GAMMA_BOUND * (1.0 + 1.0e-10)
    beta_edge_ok = beta_delta_from_x_asymptotic(VALUES["x_beta_min"]) <= BETA_BOUND * (1.0 + 1.0e-10)
    add(
        "VAL4087_GAMMA_SOLVER",
        "gamma suppression solver hits the Cassini bound",
        gamma_edge_ok,
        f"x_gamma={VALUES['x_gamma_min']:.12e}; delta={gamma_delta_from_x(VALUES['x_gamma_min']):.12e}; bound={GAMMA_BOUND:.12e}",
    )
    add(
        "VAL4087_BETA_SOLVER",
        "beta asymptotic suppression solver hits the beta bound",
        beta_edge_ok,
        f"x_beta={VALUES['x_beta_min']:.12e}; delta={beta_delta_from_x_asymptotic(VALUES['x_beta_min']):.12e}; bound={BETA_BOUND:.12e}",
    )

    stricter_beta = VALUES["x_beta_min"] > VALUES["x_gamma_min"]
    add(
        "VAL4087_STRICTER_COMPONENT",
        "combined condition selects the stricter component",
        stricter_beta and VALUES["x_combined_min"] == VALUES["x_beta_min"],
        f"x_gamma={VALUES['x_gamma_min']:.12e}; x_beta={VALUES['x_beta_min']:.12e}; x_combined={VALUES['x_combined_min']:.12e}",
    )

    smoke_rows = smoke_case_rows()
    massless = next(row for row in smoke_rows if row["case_id"] == "CASE4087_0_massless")
    screened = next(row for row in smoke_rows if row["case_id"] == "CASE4087_3_strong_screening")
    add(
        "VAL4087_SMOKE_CASES",
        "massless scalar fails and strongly screened scalar passes",
        massless["overall_pass_for_this_template"] == "False" and screened["overall_pass_for_this_template"] == "True",
        f"massless_pass={massless['overall_pass_for_this_template']}; screened_pass={screened['overall_pass_for_this_template']}",
    )

    outputs_inside_post_checkpoint = all(is_under(path, ROOT) for path in paths) and is_under(DOC_PATH, ROOT)
    outputs_outside_formalization = all(not is_under(path, FORMALIZATION) for path in paths) and not is_under(DOC_PATH, FORMALIZATION)
    add(
        "VAL4087_SCOPE",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        bool(outputs_inside_post_checkpoint and outputs_outside_formalization),
        f"doc={DOC_PATH}; csv_count={len(paths)}",
    )

    no_claim = all(row.get("valid_for_claim", "False") != "True" for row in derivation_rows())
    no_claim = no_claim and all(row.get("valid_for_claim", "False") != "True" for row in bound_rows())
    no_claim = no_claim and all(row.get("allowed") != "True" for row in claim_gate_rows() if row["claim_id"] != "CLAIM4087_2_forward_progress")
    add(
        "VAL4087_NO_LOCAL_GR_CLAIM",
        "4087 remains a private nonclaim checkpoint",
        no_claim,
        "claim gates keep R2 scalar/local-GR false until parent coefficient or zero proof exists",
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4087_SCRIPT_COMPILES", "generator script compiles", compile_ok, compile_detail)

    return checks


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4087 - First Non-EH R11 Projection Fill Gamma Beta Bound

- Timestamp: `{TIMESTAMP}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/R11 pass claim: `false`
- GitHub action: `false`

## Result

4087 fills the first live non-EH/R11 family instead of merely pointing at it.

Selected family:

```text
R2_fR_scalar_mode
f(R) subset: f(R)=R+mu R^2
m_R^2 = 1/(6 mu)
lambda_R = 1/m_R
```

The scalar mode is allowed only if it is absent, parent double-zeroed, or short-ranged enough.

## Gamma Derivation

For the standard metric `f(R)` scalar normalization:

```text
y = exp(-b/lambda_R)
gamma_R2(b) = (3-y)/(3+y)
|gamma-1| = 2y/(3+y)
```

Using the 4085 Cassini bound:

```text
B_gamma = {GAMMA_BOUND:.6e}
y <= 3 B_gamma/(2-B_gamma) = {VALUES['y_gamma_max']:.6e}
b/lambda_R >= {VALUES['x_gamma_min']:.6f}
```

With Cassini closest approach `b = 1.6 R_sun`:

```text
lambda_R <= {VALUES['lambda_gamma_rsun']:.6e} R_sun
lambda_R <= {VALUES['lambda_gamma_au']:.6e} AU
```

## Beta Derivation

The available quadratic-gravity 2PN result gives, in the scalar/f(R) limit:

```text
G_eff^2 beta - 1
  ~= (1/3) x exp(-x) ln(2x)
    + ((9 gamma_E - 4)/27) x exp(-x)

G_eff = 1 + exp(-x)/3
x = b/lambda_R
```

Solving against the 4085 beta bound:

```text
B_beta = {BETA_BOUND:.6e}
b/lambda_R >= {VALUES['x_beta_min']:.6f}
lambda_R <= {VALUES['lambda_beta_rsun']:.6e} R_sun
lambda_R <= {VALUES['lambda_beta_au']:.6e} AU
```

In this template the beta asymptotic bound is stricter than the gamma-only bound.

## Combined Bound

```text
b/lambda_R >= {VALUES['x_combined_min']:.6f}
lambda_R <= {VALUES['lambda_combined_rsun']:.6e} R_sun
lambda_R <= {VALUES['lambda_combined_m']:.6e} m
lambda_R <= {VALUES['lambda_combined_au']:.6e} AU
m_R >= {VALUES['m_inv_au']:.6e} AU^-1
mu <= {VALUES['mu_combined_m2']:.6e} m^2
```

Interpretation:

```text
long-range R2/f(R) scalar -> local GR fails
short-range enough scalar -> may survive this one family gate
parent double-zero/absence -> cleaner than bounding
```

## What This Does Not Claim

This is not an MTS local-GR pass. It is a filled bound template for one non-EH family under standard `f(R)=R+mu R^2` normalization.

To promote it, MTS must either:

```text
map c_R2 to mu and prove the bound
or prove C_i(X0)=0, dC_i(X0)=0, mass-gap, and readout silence
```

## Decision

```text
first R11 family bound = filled
gamma condition = exact for standard f(R) scalar Yukawa
beta condition = asymptotic 2PN bound template
local GR claim = still false
next = map actual MTS c_R2 or fill Ricci/Weyl spin-2 slip projection
```

## Sources

- Chiba, Smith and Erickcek, *Solar System constraints to general f(R) gravity*.
- Zhu and Li, *Parameterized post-Newtonian analysis of quadratic gravity and solar system constraints*.
- 4085 PPN bound table and 4086 non-EH projection formulas.

## Next

```text
4088-Y5-R2FR-map-MTS-cR2-normalization-or-Ricci-Weyl-spin2-slip-bound.md
```
""",
        encoding="utf-8",
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "P8_Y5_R2FR_4087_SOURCE_REGISTER.csv": source_register_rows(),
        "P8_Y5_R2FR_4087_WEB_PROVENANCE.csv": WEB_SOURCES,
        "P8_Y5_R2FR_4087_R2_SCALAR_GAMMA_BETA_DERIVATION.csv": derivation_rows(),
        "P8_Y5_R2FR_4087_R2_SCALAR_EXECUTABLE_BOUND.csv": bound_rows(),
        "P8_Y5_R2FR_4087_R2_SCALAR_SMOKE_CASES.csv": smoke_case_rows(),
        "P8_Y5_R2FR_4087_R11_VECTOR_UPDATE.csv": r11_update_rows(),
        "P8_Y5_R2FR_4087_DECISION_GATE.csv": decision_rows(),
        "P8_Y5_R2FR_4087_CLAIM_GATE.csv": claim_gate_rows(),
        "P8_Y5_R2FR_4087_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4087_STATUS.csv": status_rows(),
    }

    output_paths: List[Path] = []
    for name, rows in outputs.items():
        path = SOURCE_DIR / name
        write_csv(path, rows)
        output_paths.append(path)

    write_doc()

    validation = validation_rows(output_paths)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4087_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    shutil.rmtree(SCRIPT_PATH.parent / "__pycache__", ignore_errors=True)

    failures = [row for row in validation if row["passed"] != "True"]
    if failures:
        for failure in failures:
            print(f"VALIDATION_FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)

    print(f"4087 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")
    print(f"combined lambda_R <= {VALUES['lambda_combined_rsun']:.6e} R_sun")


if __name__ == "__main__":
    main()
