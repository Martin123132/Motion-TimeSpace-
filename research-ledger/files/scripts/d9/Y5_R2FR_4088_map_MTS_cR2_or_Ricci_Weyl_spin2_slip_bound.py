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
DOC_PATH = ROOT / "4088-Y5-R2FR-map-MTS-cR2-normalization-or-Ricci-Weyl-spin2-slip-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "MTS_CR2_MAP_NOT_PARENT_OWNED_RICCI_WEYL_SPIN2_BOUND_FILLED_GAMMA_EXACT_BETA_ASYMPTOTIC"

R_SUN_M = 6.957e8
AU_M = 149_597_870_700.0
CASSINI_IMPACT_RSUN = 1.6
GAMMA_BOUND = 2.3e-5
BETA_BOUND = 8.0e-5
EULER_GAMMA = 0.5772156649015329
HBAR_C_EV_M = 1.973269804e-7


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4088_00_4087_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4087_NEXT_TARGET.csv",
        "4088-Y5-R2FR-map-MTS-cR2-normalization-or-Ricci-Weyl-spin2-slip-bound.md",
        "4087 selects either the MTS c_R2 mapping or the Ricci/Weyl spin-2 slip bound.",
    ),
    "SRC4088_01_4087_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4087_R2_SCALAR_EXECUTABLE_BOUND.csv",
        "B4087_4_mu_coefficient_standard_fr",
        "4087 created the standard f(R) mu bound template that needs an MTS coefficient map.",
    ),
    "SRC4088_02_4087_update": (
        SOURCE_DIR / "P8_Y5_R2FR_4087_R11_VECTOR_UPDATE.csv",
        "MTS must map its c_R2 normalization to mu",
        "4087 explicitly states the remaining c_R2-to-mu promotion condition.",
    ),
    "SRC4088_03_4086_routes": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_R11_FAMILY_TO_PPN_ROUTE.csv",
        "Ricci_Weyl_squared",
        "4086 marks the Ricci/Weyl family as the neighbouring tracefree slip target.",
    ),
    "SRC4088_04_4086_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_NONEH_PPN_PROJECTION_FORMULAS.csv",
        "PROJ4086_1_gamma",
        "4086 supplies the tracefree gamma projection route.",
    ),
    "SRC4088_05_4085_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_0_gamma_cassini",
        "4085 supplies the componentwise gamma and beta bounds.",
    ),
    "SRC4088_06_2622_verdict": (
        SOURCE_DIR / "P8_Y5_LOVELOCK_GATE_2622_OPERATOR_SELECTION_VERDICT.csv",
        "OPS2622_2_Ricci_Weyl",
        "2622 already retains Ricci/Weyl as nonclaim-bound-required when Lovelock hypotheses are not parent-signed.",
    ),
    "SRC4088_07_2622_gap": (
        SOURCE_DIR / "P8_Y5_LOVELOCK_GATE_2622_PARENT_SIGNATURE_GAP_MATRIX.csv",
        "GAP2622_2_no_integrated_out_tower",
        "2622 says no integrated-out curvature tower is not derived, so curvature-square coefficients remain live.",
    ),
    "SRC4088_08_r11_executable": (
        SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv",
        "c_Ricci_or_c_Weyl",
        "The executable R11 vector still lacks parent coefficients for Ricci/Weyl.",
    ),
}


WEB_SOURCES = [
    {
        "source_id": "WEB4088_0_zhu_li_2026_quadratic_ppn",
        "title": "Parameterized post-Newtonian analysis of quadratic gravity and solar system constraints",
        "authors": "Jie Zhu, Hao Li",
        "year": "2026",
        "url": "https://link.springer.com/article/10.1140/epjc/s10052-026-15793-y",
        "source_role": "quadratic-gravity action, massive spin-2/scalar masses, gamma(r), beta(r), and solar-system constraints",
        "extracted_result": "Action R-lambda C^2+mu R^2; m_W^2=1/(2 lambda), m_R^2=1/(6 mu); gamma(r)=(3-exp(-m_R r)-2exp(-m_W r))/(3+exp(-m_R r)-4exp(-m_W r)); pure Weyl gamma bound m_W >= about 1200 AU^-1 is reported.",
        "confidence": "open_access_Eur_Phys_J_C_article",
        "timestamp_utc": TIMESTAMP,
    },
    {
        "source_id": "WEB4088_1_quadratic_potential_lineage",
        "title": "Classical Gravity with Higher Derivatives",
        "authors": "K. S. Stelle",
        "year": "1977",
        "url": "https://inspirehep.net/literature/119488",
        "source_role": "lineage for quadratic curvature terms producing massive scalar and spin-2 sectors",
        "extracted_result": "Including R_munu R^munu and R^2 terms gives a multi-mass modification of classical gravity.",
        "confidence": "literature_index_for_primary_Stelle_lineage",
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


def gamma_spin2_delta(x_value: float) -> float:
    y_value = math.exp(-x_value)
    return abs((3.0 - 2.0 * y_value) / (3.0 - 4.0 * y_value) - 1.0)


def beta_spin2_delta_asymptotic(x_value: float) -> float:
    y_value = math.exp(-x_value)
    geff = 1.0 - (4.0 / 3.0) * y_value
    beta_geff2 = (
        1.0
        - (4.0 / 3.0) * x_value * y_value * math.log(2.0 * x_value)
        - ((36.0 * EULER_GAMMA + 13.0) / 27.0) * x_value * y_value
    )
    return abs(beta_geff2 / (geff * geff) - 1.0)


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
    impact_m = CASSINI_IMPACT_RSUN * R_SUN_M
    impact_au = impact_m / AU_M
    y_gamma_max = (3.0 * GAMMA_BOUND) / (2.0 + 4.0 * GAMMA_BOUND)
    x_gamma_min = -math.log(y_gamma_max)
    x_beta_min = solve_x_for_bound(beta_spin2_delta_asymptotic, BETA_BOUND)
    x_combined_min = max(x_gamma_min, x_beta_min)

    lambda_gamma_rsun = CASSINI_IMPACT_RSUN / x_gamma_min
    lambda_beta_rsun = CASSINI_IMPACT_RSUN / x_beta_min
    lambda_combined_rsun = CASSINI_IMPACT_RSUN / x_combined_min
    lambda_combined_m = lambda_combined_rsun * R_SUN_M
    lambda_combined_au = lambda_combined_m / AU_M
    lambda_weyl_coeff_m2 = lambda_combined_m**2 / 2.0
    m_inv_au = 1.0 / lambda_combined_au
    m_inv_m = 1.0 / lambda_combined_m
    m_energy_ev = HBAR_C_EV_M / lambda_combined_m

    return {
        "impact_m": impact_m,
        "impact_au": impact_au,
        "y_gamma_max": y_gamma_max,
        "x_gamma_min": x_gamma_min,
        "x_beta_min": x_beta_min,
        "x_combined_min": x_combined_min,
        "lambda_gamma_rsun": lambda_gamma_rsun,
        "lambda_beta_rsun": lambda_beta_rsun,
        "lambda_combined_rsun": lambda_combined_rsun,
        "lambda_combined_m": lambda_combined_m,
        "lambda_combined_au": lambda_combined_au,
        "lambda_weyl_coeff_m2": lambda_weyl_coeff_m2,
        "m_inv_au": m_inv_au,
        "m_inv_m": m_inv_m,
        "m_energy_ev": m_energy_ev,
        "gamma_at_combined": gamma_spin2_delta(x_combined_min),
        "beta_at_combined": beta_spin2_delta_asymptotic(x_combined_min),
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
                "source_type": "web_literature",
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
            "source_id": "SRC4088_09_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for c_R2 mapping audit and Ricci/Weyl spin-2 slip bound.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def cr2_mapping_audit_rows() -> List[dict]:
    return [
        {
            "audit_id": "CR2MAP4088_0_standard_template",
            "target": "map MTS c_R2 to standard mu in f(R)=R+mu R^2",
            "evidence": "4087 provides mu <= lambda_R^2/6 under standard metric f(R) normalization.",
            "result": "TEMPLATE_EXISTS",
            "promotion_status": "NOT_PARENT_OWNED",
            "reason": "A template bound is not a coefficient map from the MTS parent action.",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "audit_id": "CR2MAP4088_1_r11_executable",
            "target": "find parent numeric c_R2_or_c_fR",
            "evidence": "R11_nonEH_operator_vector_executable still carries MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT for R2_fR_scalar_mode.",
            "result": "NO_PARENT_NUMERIC_COEFFICIENT_FOUND",
            "promotion_status": "BLOCKED_FOR_R2_PARENT_BOUND",
            "reason": "The coefficient value, units, length normalization and source path are still missing in the executable vector.",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "audit_id": "CR2MAP4088_2_integrated_out_tower",
            "target": "prove no eliminated sector regenerates R2/f(R)",
            "evidence": "2622 gap matrix marks no_integrated_out_tower as NOT_DERIVED.",
            "result": "NO_GLOBAL_ZERO_THEOREM_FOUND",
            "promotion_status": "R2_FAMILY_RETAINS_BOUND_ROUTE",
            "reason": "A second-order parent can still generate observed higher-curvature terms after solving hidden variables unless this theorem is signed.",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "audit_id": "CR2MAP4088_3_decision",
            "target": "choose 4088 working branch",
            "evidence": "c_R2 map absent; 4086 routes Ricci_Weyl_squared to tracefree gamma slip; Zhu/Li source gives m_W and gamma/beta formulas.",
            "result": "PIVOT_TO_RICCI_WEYL_SPIN2_SLIP_BOUND",
            "promotion_status": "FORWARD_PROGRESS_BRANCH_SELECTED",
            "reason": "Do not stall on absent c_R2 parent map; fill the sibling Weyl spin-2 bound.",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def spin2_derivation_rows() -> List[dict]:
    return [
        {
            "row_id": "RW4088_0_family_selection",
            "piece": "Ricci/Weyl spin-2 family",
            "statement": "Select the Ricci/Weyl squared family, represented in the Zhu/Li convention by the Weyl coefficient lambda in L proportional to R-lambda C^2+mu R^2.",
            "formula": "m_W^2=1/(2 lambda_Weyl); y_W=exp(-m_W b)",
            "derived_result": "RICCI_WEYL_SPIN2_MODE_SELECTED",
            "status": "EXECUTABLE_NONCLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "RW4088_1_gamma_formula",
            "piece": "spin-2 gamma projection",
            "statement": "In the pure Weyl/spin-2 limit m_R -> infinity, Zhu/Li gamma(r) reduces to gamma_W=(3-2y_W)/(3-4y_W).",
            "formula": "gamma_W(b)=(3-2exp(-b/lambda_W))/(3-4exp(-b/lambda_W))",
            "derived_result": "EXACT_SPIN2_YUKAWA_GAMMA_FORMULA",
            "status": "DERIVED_FROM_ZHU_LI_GAMMA",
            "numeric_value": "",
            "units": "",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "RW4088_2_gamma_suppression",
            "piece": "Cassini gamma condition",
            "statement": "For y_W<3/4, the gamma residual is 2y_W/(3-4y_W). Imposing B_gamma gives y_W <= 3B_gamma/(2+4B_gamma).",
            "formula": "exp(-b/lambda_W) <= 3B_gamma/(2+4B_gamma)",
            "derived_result": "EXACT_SPIN2_GAMMA_SUPPRESSION_INEQUALITY",
            "status": "NUMERIC_BOUND_FILLED",
            "numeric_value": f"{VALUES['x_gamma_min']:.12e}",
            "units": "minimum_b_over_lambda_from_gamma",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "RW4088_3_beta_asymptotic",
            "piece": "spin-2 beta projection",
            "statement": "In the pure Weyl limit m_R -> infinity, the sourced quadratic-gravity asymptotic gives G_eff^2 beta-1 as a negative spin-2 Yukawa log term plus a negative x exp(-x) coefficient term.",
            "formula": "G_eff^2 beta - 1 ~= -(4/3)x e^-x ln(2x) - ((36 gamma_E+13)/27)x e^-x; G_eff=1-4e^-x/3",
            "derived_result": "ASYMPTOTIC_SPIN2_BETA_BOUND_FORMULA",
            "status": "ASYMPTOTIC_NUMERIC_BOUND_FILLED",
            "numeric_value": f"{VALUES['x_beta_min']:.12e}",
            "units": "minimum_b_over_lambda_from_beta_asymptotic",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "RW4088_4_combined_condition",
            "piece": "combined spin-2 local PPN condition",
            "statement": "The spin-2 Weyl/Ricci family survives this template only if x=b/lambda_W is at least the stricter gamma/beta threshold, or if the parent proves topological absence/double-zero.",
            "formula": "x >= max(x_gamma_min,x_beta_min)",
            "derived_result": "COMBINED_RICCI_WEYL_SPIN2_LOCAL_PPN_BOUND",
            "status": "NUMERIC_BOUND_FILLED_NONCLAIM",
            "numeric_value": f"{VALUES['x_combined_min']:.12e}",
            "units": "minimum_b_over_lambda",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def spin2_bound_rows() -> List[dict]:
    return [
        {
            "bound_id": "B4088_0_spin2_gamma_yukawa_amplitude",
            "mode": "Ricci_Weyl_squared_spin2",
            "observable": "gamma_minus_1",
            "bound_input": f"{GAMMA_BOUND:.12e}",
            "bound_input_units": "dimensionless",
            "derived_condition": "exp(-b/lambda_W) <= 3B_gamma/(2+4B_gamma)",
            "numeric_value": f"{VALUES['y_gamma_max']:.12e}",
            "numeric_units": "max_yukawa_factor_yW",
            "source": "4085 Cassini gamma bound plus Zhu/Li pure Weyl gamma formula",
            "status": "EXACT_SPIN2_GAMMA_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4088_1_spin2_gamma_range",
            "mode": "Ricci_Weyl_squared_spin2",
            "observable": "lambda_W_gamma_only",
            "bound_input": f"{CASSINI_IMPACT_RSUN:.12e}",
            "bound_input_units": "solar_radii Cassini impact parameter",
            "derived_condition": "lambda_W <= b/x_gamma_min",
            "numeric_value": f"{CASSINI_IMPACT_RSUN / VALUES['x_gamma_min']:.12e}",
            "numeric_units": "solar_radii",
            "numeric_value_m": f"{(CASSINI_IMPACT_RSUN / VALUES['x_gamma_min']) * R_SUN_M:.12e}",
            "numeric_value_au": f"{((CASSINI_IMPACT_RSUN / VALUES['x_gamma_min']) * R_SUN_M) / AU_M:.12e}",
            "status": "GAMMA_ONLY_SPIN2_RANGE_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4088_2_spin2_beta_range_asymptotic",
            "mode": "Ricci_Weyl_squared_spin2",
            "observable": "lambda_W_beta_asymptotic",
            "bound_input": f"{BETA_BOUND:.12e}",
            "bound_input_units": "dimensionless",
            "derived_condition": "abs(beta_W_asymptotic(x)-1) <= B_beta",
            "numeric_value": f"{CASSINI_IMPACT_RSUN / VALUES['x_beta_min']:.12e}",
            "numeric_units": "solar_radii",
            "numeric_value_m": f"{(CASSINI_IMPACT_RSUN / VALUES['x_beta_min']) * R_SUN_M:.12e}",
            "numeric_value_au": f"{((CASSINI_IMPACT_RSUN / VALUES['x_beta_min']) * R_SUN_M) / AU_M:.12e}",
            "status": "BETA_ASYMPTOTIC_SPIN2_RANGE_BOUND_NONCLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4088_3_spin2_combined_range",
            "mode": "Ricci_Weyl_squared_spin2",
            "observable": "lambda_W_combined_gamma_beta",
            "bound_input": "max(gamma threshold,beta asymptotic threshold)",
            "bound_input_units": "componentwise PPN",
            "derived_condition": "lambda_W <= b/max(x_gamma,x_beta)",
            "numeric_value": f"{VALUES['lambda_combined_rsun']:.12e}",
            "numeric_units": "solar_radii",
            "numeric_value_m": f"{VALUES['lambda_combined_m']:.12e}",
            "numeric_value_au": f"{VALUES['lambda_combined_au']:.12e}",
            "status": "STRICTER_BETA_ASYMPTOTIC_SPIN2_BOUND_SELECTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4088_4_weyl_coefficient_zhu_li",
            "mode": "Ricci_Weyl_squared_spin2",
            "observable": "lambda_Weyl_coefficient",
            "bound_input": "m_W^2=1/(2 lambda_Weyl), lambda_range=1/m_W",
            "bound_input_units": "Zhu/Li convention L proportional to R-lambda C^2+mu R^2",
            "derived_condition": "lambda_Weyl <= lambda_range^2/2",
            "numeric_value": f"{VALUES['lambda_weyl_coeff_m2']:.12e}",
            "numeric_units": "m^2",
            "status": "STANDARD_WEYL_NORMALIZATION_COEFFICIENT_BOUND_TEMPLATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4088_5_spin2_mass_scale",
            "mode": "Ricci_Weyl_squared_spin2",
            "observable": "m_W_min",
            "bound_input": "1/lambda_W_combined",
            "bound_input_units": "inverse length",
            "derived_condition": "m_W >= max(x_gamma,x_beta)/b",
            "numeric_value": f"{VALUES['m_inv_au']:.12e}",
            "numeric_units": "AU^-1",
            "numeric_value_m_inv": f"{VALUES['m_inv_m']:.12e}",
            "numeric_value_energy_ev": f"{VALUES['m_energy_ev']:.12e}",
            "status": "SPIN2_MASS_SCALE_TRANSLATION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def smoke_case_rows() -> List[dict]:
    cases = [
        ("CASE4088_0_massless_spin2", 0.0, "massless_or_solar_system_long_range_spin2"),
        ("CASE4088_1_gamma_edge", VALUES["x_gamma_min"], "gamma_bound_edge"),
        ("CASE4088_2_beta_edge", VALUES["x_beta_min"], "beta_bound_edge"),
        ("CASE4088_3_strong_screening", 20.0, "comfortably_short_range_spin2"),
    ]
    rows: List[dict] = []
    for case_id, x_value, meaning in cases:
        gamma_delta = gamma_spin2_delta(x_value)
        beta_delta = beta_spin2_delta_asymptotic(x_value) if x_value > 0.0 else float("inf")
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
            "update_id": "R11UP4088_0",
            "operator_family": "R2_fR_scalar_mode",
            "old_status": "NORMALIZATION_TEMPLATE_READY_NOT_PARENT_COEFFICIENT",
            "new_status": "UNCHANGED_PARENT_CR2_MAP_MISSING",
            "zero_or_bound": "4087 bound template retained but not promoted",
            "condition_to_pass": "map actual MTS c_R2 to standard mu or prove R2/f(R) absent/double-zero",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "R11UP4088_1",
            "operator_family": "Ricci_Weyl_squared",
            "old_status": "HIGH_PRIORITY_TRACEFREE_SLIP_FILL",
            "new_status": "FILLED_STANDARD_WEYL_SPIN2_GAMMA_BETA_BOUND_TEMPLATE",
            "zero_or_bound": "bound unless parent proves topological/absent/double-zero",
            "condition_to_pass": f"lambda_W <= {VALUES['lambda_combined_rsun']:.6e} R_sun for pure Weyl spin-2 template, or parent topological/zero proof",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4088_0_main",
            "decision": DECISION,
            "meaning": "The actual MTS c_R2 normalization is still absent, so 4088 fills the neighbouring Ricci/Weyl massive spin-2 bound rather than stalling. Two curvature-square families now have executable bound templates.",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_required_move": "Either map MTS curvature-square coefficients into mu/lambda_Weyl, or move to projector/domain stress because that is now the harsher local-GR branch.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4088_1_physics_read",
            "decision": "LONG_RANGE_SPIN2_WEYL_BRANCH_FAILS_LOCAL_GR",
            "meaning": "A long-range Weyl/Ricci massive spin-2 mode gives gamma and beta deviations. MTS keeps this route only by topological absence, double-zero, mass gap/screening, or an explicit parent coefficient below the bound.",
            "claim_status": "DISCIPLINE_RULE",
            "next_required_move": "Do not call local GR while this coefficient is unmapped.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4088_0_cR2_map",
            "claim": "MTS c_R2 maps to the standard f(R) mu slot",
            "allowed": "False",
            "why_not": "No parent-owned coefficient value, units, normalization or source path was found.",
            "minimum_unlock": "Provide parent action normalization showing c_R2=mu or a conversion factor with units and sign.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4088_1_spin2_pass",
            "claim": "MTS Ricci/Weyl spin-2 family passes local PPN",
            "allowed": "False",
            "why_not": "4088 gives a standard Weyl spin-2 bound template, not a parent-owned MTS c_Ricci/c_Weyl coefficient.",
            "minimum_unlock": "Map MTS c_Ricci/c_Weyl to the Zhu/Li lambda_Weyl convention or prove topological/absent/double-zero.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4088_2_local_GR",
            "claim": "MTS reduces to local GR",
            "allowed": "False",
            "why_not": "Only two curvature-square families have bound templates; source, projector, vector, torsion and readout branches remain live.",
            "minimum_unlock": "All 4086 R11 family rows zeroed or bounded with source/readout/conservation gates.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4088_3_forward_progress",
            "claim": "4088 advances the framework",
            "allowed": "True_private_checkpoint",
            "why_not": "Private derived/bounded checkpoint only.",
            "minimum_unlock": "N/A",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4088_0",
            "next_target": "4089-Y5-R2FR-curvature-square-coefficient-map-or-projector-domain-stress-bound.md",
            "script": "scripts/Y5_R2FR_4089_curvature_square_coeff_map_or_projector_domain_stress_bound.py",
            "why": "R2 and Weyl spin-2 now have standard bound templates. The next best move is either map actual MTS curvature-square coefficients, or attack the projector/domain stress branch because it feeds gamma, beta, alpha_i, xi and zeta_i.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4088_1",
            "next_target": "ZhuLi_joint_mR_mW_contour_import",
            "script": "defer_until_needed",
            "why": "The separate scalar/spin2 templates are conservative branch rows; a future joint contour can capture cancellation/degeneneracy only if parent signs a non-tuned relation such as m_R=m_W.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4088",
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
            f"VAL4088_SRC_{source_id}",
            "local source exists and contains needle",
            bool(exists and contains),
            f"{path} | needle={needle} | role={role}",
        )

    for path in paths:
        rows = parse_csv(path)
        add(
            f"VAL4088_CSV_{path.stem}",
            "generated CSV parses and is non-empty",
            bool(rows),
            f"{path} rows={len(rows)}",
        )

    c_map_rows = cr2_mapping_audit_rows()
    no_parent_map = any(row["result"] == "NO_PARENT_NUMERIC_COEFFICIENT_FOUND" for row in c_map_rows)
    pivot = any(row["result"] == "PIVOT_TO_RICCI_WEYL_SPIN2_SLIP_BOUND" for row in c_map_rows)
    add(
        "VAL4088_CR2_AUDIT_DECISION",
        "c_R2 mapping audit blocks promotion and selects spin2 branch",
        no_parent_map and pivot,
        f"no_parent_map={no_parent_map}; pivot={pivot}",
    )

    gamma_edge_ok = gamma_spin2_delta(VALUES["x_gamma_min"]) <= GAMMA_BOUND * (1.0 + 1.0e-10)
    beta_edge_ok = beta_spin2_delta_asymptotic(VALUES["x_beta_min"]) <= BETA_BOUND * (1.0 + 1.0e-10)
    add(
        "VAL4088_GAMMA_SOLVER",
        "spin2 gamma suppression solver hits the Cassini bound",
        gamma_edge_ok,
        f"x_gamma={VALUES['x_gamma_min']:.12e}; delta={gamma_spin2_delta(VALUES['x_gamma_min']):.12e}; bound={GAMMA_BOUND:.12e}",
    )
    add(
        "VAL4088_BETA_SOLVER",
        "spin2 beta asymptotic suppression solver hits the beta bound",
        beta_edge_ok,
        f"x_beta={VALUES['x_beta_min']:.12e}; delta={beta_spin2_delta_asymptotic(VALUES['x_beta_min']):.12e}; bound={BETA_BOUND:.12e}",
    )

    smoke_rows = smoke_case_rows()
    massless = next(row for row in smoke_rows if row["case_id"] == "CASE4088_0_massless_spin2")
    screened = next(row for row in smoke_rows if row["case_id"] == "CASE4088_3_strong_screening")
    add(
        "VAL4088_SMOKE_CASES",
        "massless spin2 fails and strongly screened spin2 passes",
        massless["overall_pass_for_this_template"] == "False" and screened["overall_pass_for_this_template"] == "True",
        f"massless_pass={massless['overall_pass_for_this_template']}; screened_pass={screened['overall_pass_for_this_template']}",
    )

    outputs_inside_post_checkpoint = all(is_under(path, ROOT) for path in paths) and is_under(DOC_PATH, ROOT)
    outputs_outside_formalization = all(not is_under(path, FORMALIZATION) for path in paths) and not is_under(DOC_PATH, FORMALIZATION)
    add(
        "VAL4088_SCOPE",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        bool(outputs_inside_post_checkpoint and outputs_outside_formalization),
        f"doc={DOC_PATH}; csv_count={len(paths)}",
    )

    no_claim = all(row.get("valid_for_claim", "False") != "True" for row in cr2_mapping_audit_rows())
    no_claim = no_claim and all(row.get("valid_for_claim", "False") != "True" for row in spin2_derivation_rows())
    no_claim = no_claim and all(row.get("valid_for_claim", "False") != "True" for row in spin2_bound_rows())
    no_claim = no_claim and all(row.get("allowed") != "True" for row in claim_gate_rows() if row["claim_id"] != "CLAIM4088_3_forward_progress")
    add(
        "VAL4088_NO_LOCAL_GR_CLAIM",
        "4088 remains a private nonclaim checkpoint",
        no_claim,
        "claim gates keep c_R2, spin2 and local-GR claims false until parent coefficient/zero proof exists",
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4088_SCRIPT_COMPILES", "generator script compiles", compile_ok, compile_detail)

    return checks


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4088 - Map MTS cR2 Normalization Or Ricci Weyl Spin2 Slip Bound

- Timestamp: `{TIMESTAMP}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/R11 pass claim: `false`
- GitHub action: `false`

## Result

4088 tried the direct `c_R2 -> mu` promotion first. The corpus still does not contain a parent-owned coefficient map:

```text
MTS c_R2 value: missing
units/normalization: missing
source path: missing
parent zero theorem: missing
```

So 4088 pivots to the sibling curvature-square family and fills the Ricci/Weyl massive spin-2 slip bound.

## cR2 Mapping Audit

4087 produced:

```text
f(R)=R+mu R^2
m_R^2=1/(6 mu)
mu <= lambda_R^2/6
```

But this is only a standard-normalization template. It becomes an MTS result only after:

```text
c_R2 = conversion_factor * mu
```

with parent-owned units, sign, frame, and source path. That map was not found.

## Spin-2 Gamma Bound

For the Zhu/Li convention:

```text
L proportional to R - lambda_W C^2 + mu R^2
m_W^2 = 1/(2 lambda_W)
```

In the pure Weyl/spin-2 limit:

```text
y_W = exp(-b/lambda_W_range)
gamma_W = (3 - 2 y_W)/(3 - 4 y_W)
|gamma_W - 1| = 2 y_W/(3 - 4 y_W)
```

Using the 4085 Cassini bound:

```text
B_gamma = {GAMMA_BOUND:.6e}
y_W <= {VALUES['y_gamma_max']:.6e}
b/lambda_W >= {VALUES['x_gamma_min']:.6f}
```

## Spin-2 Beta Bound

Using the pure Weyl asymptotic 2PN result:

```text
G_eff = 1 - (4/3) exp(-x)
G_eff^2 beta - 1
  ~= -(4/3) x exp(-x) ln(2x)
     - ((36 gamma_E + 13)/27) x exp(-x)
```

Solving against the 4085 beta bound:

```text
B_beta = {BETA_BOUND:.6e}
b/lambda_W >= {VALUES['x_beta_min']:.6f}
```

This beta-asymptotic condition is stricter in this template.

## Combined Bound

With `b = 1.6 R_sun`:

```text
b/lambda_W >= {VALUES['x_combined_min']:.6f}
lambda_W_range <= {VALUES['lambda_combined_rsun']:.6e} R_sun
lambda_W_range <= {VALUES['lambda_combined_m']:.6e} m
lambda_W_range <= {VALUES['lambda_combined_au']:.6e} AU
m_W >= {VALUES['m_inv_au']:.6e} AU^-1
lambda_Weyl_coeff <= {VALUES['lambda_weyl_coeff_m2']:.6e} m^2
```

Interpretation:

```text
long-range Ricci/Weyl spin-2 mode -> local GR fails
short-range enough mode -> survives this one family gate
topological/absent/double-zero proof -> cleaner than bounding
```

## What This Does Not Claim

This does not prove MTS local GR. It gives a standard Weyl spin-2 bound template.

To promote it, MTS must map:

```text
c_Ricci/c_Weyl -> lambda_Weyl
```

or prove the Ricci/Weyl sector is topological, absent, or auxiliary double-zero with readout silence.

## Decision

```text
c_R2 parent map = not found
R2 scalar template = retained but not promoted
Ricci/Weyl spin-2 gamma/beta template = filled
local GR claim = still false
next = coefficient map or projector/domain stress bound
```

## Sources

- Zhu and Li, *Parameterized post-Newtonian analysis of quadratic gravity and solar system constraints*.
- Stelle, *Classical Gravity with Higher Derivatives*.
- 4085 PPN bounds, 4086 projection formulas, 4087 scalar-mode bound.

## Next

```text
4089-Y5-R2FR-curvature-square-coefficient-map-or-projector-domain-stress-bound.md
```
""",
        encoding="utf-8",
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "P8_Y5_R2FR_4088_SOURCE_REGISTER.csv": source_register_rows(),
        "P8_Y5_R2FR_4088_WEB_PROVENANCE.csv": WEB_SOURCES,
        "P8_Y5_R2FR_4088_CR2_MAPPING_AUDIT.csv": cr2_mapping_audit_rows(),
        "P8_Y5_R2FR_4088_RICCI_WEYL_SPIN2_DERIVATION.csv": spin2_derivation_rows(),
        "P8_Y5_R2FR_4088_RICCI_WEYL_SPIN2_EXECUTABLE_BOUND.csv": spin2_bound_rows(),
        "P8_Y5_R2FR_4088_RICCI_WEYL_SPIN2_SMOKE_CASES.csv": smoke_case_rows(),
        "P8_Y5_R2FR_4088_R11_VECTOR_UPDATE.csv": r11_update_rows(),
        "P8_Y5_R2FR_4088_DECISION_GATE.csv": decision_rows(),
        "P8_Y5_R2FR_4088_CLAIM_GATE.csv": claim_gate_rows(),
        "P8_Y5_R2FR_4088_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4088_STATUS.csv": status_rows(),
    }

    output_paths: List[Path] = []
    for name, rows in outputs.items():
        path = SOURCE_DIR / name
        write_csv(path, rows)
        output_paths.append(path)

    write_doc()

    validation = validation_rows(output_paths)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4088_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    shutil.rmtree(SCRIPT_PATH.parent / "__pycache__", ignore_errors=True)

    failures = [row for row in validation if row["passed"] != "True"]
    if failures:
        for failure in failures:
            print(f"VALIDATION_FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)

    print(f"4088 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")
    print(f"combined lambda_W <= {VALUES['lambda_combined_rsun']:.6e} R_sun")


if __name__ == "__main__":
    main()
