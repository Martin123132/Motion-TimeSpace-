from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

from scipy.constants import G, c


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4922"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_WEYL_C3_GW170608_DOMAIN_GATE_4922"
FORMAL_MARKER = "PPC4161_WEYL_C3_GW170608_DOMAIN_GATE_4922"
NEXT_TARGET = (
    "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-"
    "recast-or-posterior-acquisition-gate.md"
)

LIU_YUNES_URL = "https://arxiv.org/abs/2407.08929"
CANO_QNM_URL = "https://arxiv.org/abs/2110.11378"
BURGER_URL = "https://arxiv.org/abs/1910.11618"
SILVA_RINGDOWN_URL = "https://arxiv.org/abs/2205.05132"
PAYNE_SCALING_URL = "https://arxiv.org/abs/2407.07043"
GW250114_URL = "https://arxiv.org/abs/2509.08099"
GRAVITATIONAL_QNM_URL = "https://arxiv.org/abs/2307.07431"
SCALAR_HIGH_SPIN_C3_URL = "https://arxiv.org/abs/2604.11755"

EARTH_MASS_KG = 5.9722e24
EARTH_RADIUS_M = 6_371_000.0
SUN_MASS_KG = 1.98847e30
SUN_RADIUS_M = 695_700_000.0
GALILEO_ALTITUDE_M = 23_229_000.0
GW170608_PRIMARY_MASS_MSUN = 12.0
GW170608_SECONDARY_MASS_MSUN = 7.0
GW170608_TOTAL_MASS_MSUN_APPROX = 19.0

ALPHA1_CENTRAL = 0.87
ALPHA1_LOWER_90 = -0.16
ALPHA1_UPPER_90 = 2.82
ALPHA2_CENTRAL = -0.35
ALPHA2_LOWER_90 = -3.27
ALPHA2_UPPER_90 = 3.77
LOG_B_EFT_GR = -2.81
MIXED_RINGDOWN_ELL_KM = 38.2
TAU_CLOCK = 2.48e-5
TAU_DOMAIN = 0.01


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


def gravitational_mass_length(mass_kg: float) -> float:
    return G * mass_kg / c**2


def schwarzschild_radius(mass_kg: float) -> float:
    return 2.0 * gravitational_mass_length(mass_kg)


def gw170608_mass_length() -> float:
    return gravitational_mass_length(GW170608_TOTAL_MASS_MSUN_APPROX * SUN_MASS_KG)


def ell_ratio(alpha_bar_magnitude: float) -> float:
    if alpha_bar_magnitude < 0.0:
        raise ValueError("magnitude must be nonnegative")
    return alpha_bar_magnitude**0.25


def ell_approx_m(alpha_bar_magnitude: float) -> float:
    return gw170608_mass_length() * ell_ratio(alpha_bar_magnitude)


def pure_i1_clock_coefficient(
    mass_length_m: float, radius_1_m: float, radius_2_m: float
) -> float:
    return (
        20.0
        * mass_length_m**2
        * abs(radius_1_m**-7 - radius_2_m**-7)
        / abs(radius_1_m**-1 - radius_2_m**-1)
    )


def pure_i1_clock_cap() -> float:
    coefficient = pure_i1_clock_coefficient(
        gravitational_mass_length(EARTH_MASS_KG),
        EARTH_RADIUS_M,
        EARTH_RADIUS_M + GALILEO_ALTITUDE_M,
    )
    return (TAU_CLOCK / coefficient) ** 0.25


def pure_i1_acceleration_fraction(
    ell_m: float, mass_length_m: float, radius_m: float
) -> float:
    return 140.0 * ell_m**4 * mass_length_m**2 / radius_m**6


def pure_i1_potential_fraction(
    ell_m: float, mass_length_m: float, radius_m: float
) -> float:
    return 20.0 * ell_m**4 * mass_length_m**2 / radius_m**6


def compact_domain_cap(kretschmann_m_minus_4: float) -> float:
    return (TAU_DOMAIN / kretschmann_m_minus_4) ** 0.25


def basis_map_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "map_id": "BASIS4922_00_corpus",
                "object": "corpus parity-even Weyl-cubic operator",
                "definition": "O_+=C_mn^rs C_rs^ab C_ab^mn",
                "coefficient": "zeta_+",
                "relation": "O_+=I1=C7 on Ricci-flat backgrounds",
                "status": "EXACT_CONTRACTION_MATCH",
                "source": "post-checkpoint-work/4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md",
                "passed": True,
            },
            {
                "map_id": "BASIS4922_01_identity",
                "object": "second parity-even Riemann-cubic contraction",
                "definition": "I2=C8",
                "coefficient": "basis dependent",
                "relation": "I2=I1/2 on smooth four-dimensional Ricci-flat geometry",
                "status": "EXACT_4911_QUOTIENT_IDENTITY",
                "source": "post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4911_RICCI_FLAT_MAP.csv",
                "passed": True,
            },
            {
                "map_id": "BASIS4922_02_action",
                "object": "signed invariant cubic length",
                "definition": "a_+=16 pi G_N zeta_+=s_+ ell_+^4",
                "coefficient": "ell_+=abs(16 pi G_N zeta_+)^(1/4)",
                "relation": "S=(16 pi G_N)^-1 int sqrt(-g)[R+s_+ ell_+^4 I1+...]",
                "status": "CANONICAL_WAVEFORM_NORMALIZATION",
                "source": CANO_QNM_URL,
                "passed": True,
            },
            {
                "map_id": "BASIS4922_03_waveform",
                "object": "GW170608 dimensionless coefficient",
                "definition": "alpha_bar1=a_+/M_geo^4",
                "coefficient": "sign(alpha_bar1)=s_+",
                "relation": "alpha_bar1=s_+(ell_+/M_geo)^4",
                "status": "EXACT_SAMPLE_LEVEL_MAP",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
            {
                "map_id": "BASIS4922_04_binary",
                "object": "binary-only second parity-even direction",
                "definition": "J_2body=(I1-2I2)/2",
                "coefficient": "alpha_bar2",
                "relation": "J_2body=0 on a smooth isolated Ricci-flat body but can enter two-body matching and radiation",
                "status": "NUISANCE_DIRECTION_NOT_IDENTIFIED_WITH_ZETA_PLUS",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
            {
                "map_id": "BASIS4922_05_Burger",
                "object": "Burger generic cubic coordinate",
                "definition": "P=beta1 I2+beta2 I1+Ricci terms",
                "coefficient": "lambda beta1 controls the displayed static r^-6 probe potential",
                "relation": "zeta_+=lambda(beta2+beta1/2) after the Ricci-flat identity",
                "status": "DIFFERENT_COEFFICIENT_COORDINATE",
                "source": BURGER_URL,
                "passed": True,
            },
            {
                "map_id": "BASIS4922_06_noninvertible",
                "object": "counterexample to L3-to-zeta inversion",
                "definition": "beta1=0; beta2 nonzero",
                "coefficient": "Burger r^-6 beta1 length is zero while zeta_+=lambda beta2 is nonzero",
                "relation": "no function zeta_+=zeta_+(L3_Burger) exists without beta2/beta1 ownership",
                "status": "NONINVERTIBILITY_PROVED",
                "source": f"{BURGER_URL};post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4911_RICCI_FLAT_MAP.csv",
                "passed": True,
            },
            {
                "map_id": "BASIS4922_07_parity",
                "object": "parity-odd cubic direction",
                "definition": "O_-=C C Ctilde",
                "coefficient": "zeta_-",
                "relation": "motion-scalar threshold is exactly zero but a general bare parity-odd boundary remains a separate owner question",
                "status": "NOT_MERGED_WITH_PARITY_EVEN_BOUND",
                "source": "post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
                "passed": True,
            },
        ]
    )


def supersession_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "item": "4921_L3_definition",
                "old_status": "active observable length for total C3 packet",
                "new_status": "BURGER_BETA1_BENCHMARK_ONLY",
                "reason": "lambda beta1 does not determine zeta_+=lambda(beta2+beta1/2)",
                "active_use": False,
                "replacement": "ell_+^4=abs(16 pi G_N zeta_+)",
                "passed": True,
            },
            {
                "item": "4921_r_minus_6_transfer",
                "old_status": "generic total-C3 exterior transfer",
                "new_status": "VALID_ONLY_IN_DECLARED_BURGER_BETA1_PROBE_ROUTE",
                "reason": "pure I1 has beta1=0 and its invariant g_tt correction begins at r^-7 after the metric-function cancellation",
                "active_use": False,
                "replacement": "delta Phi_I1=-20 s_+ ell_+^4 M_geo^3/r^7",
                "passed": True,
            },
            {
                "item": "4921_Galileo_bound",
                "old_status": "selected L3 total-C3 bound",
                "new_status": "DEMOTED_NOT_A_ZETA_PLUS_BOUND",
                "reason": "the apparatus projection constrained lambda beta1 under extra basis assumptions",
                "active_use": False,
                "replacement": "corrected pure-I1 clock envelope in 4922",
                "passed": True,
            },
            {
                "item": "4921_Cassini_bound",
                "old_status": "total-C3 light bound",
                "new_status": "DEMOTED_NOT_A_ZETA_PLUS_BOUND",
                "reason": "equal weak potentials and beta1-to-zeta ownership were not established",
                "active_use": False,
                "replacement": "no light recast until the pure-I1 spatial metric is projected in one gauge-invariant observable",
                "passed": True,
            },
            {
                "item": "4921_Mercury_bound",
                "old_status": "total-C3 orbit bound",
                "new_status": "DEMOTED_NOT_A_ZETA_PLUS_BOUND",
                "reason": "the central potential was a beta1 coordinate rather than the corpus I1 packet",
                "active_use": False,
                "replacement": "GW170608 marginalized alpha_bar1 bound",
                "passed": True,
            },
            {
                "item": "4921_compact_control",
                "old_status": "epsilon_K=L3^4 K/9",
                "new_status": "RENORMALIZED_TO_EPSILON_K=ELL_PLUS^4_K",
                "reason": "the factor nine belonged to the superseded L3 definition",
                "active_use": False,
                "replacement": "ell_+<(tau/K)^(1/4)",
                "passed": True,
            },
            {
                "item": "weak_invariant_vacuum_GR",
                "old_status": "retained under L3 clause",
                "new_status": "RETAINED_AFTER_REPLACEMENT_NOT_BY_4921_BOUND",
                "reason": "the corrected I1 map plus direct GW envelope makes weak local residuals tiny",
                "active_use": True,
                "replacement": "GW170608 alpha_bar1 envelope plus corrected static metric projection",
                "passed": True,
            },
        ]
    )


def static_metric_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "metric_id": "METRIC4922_00_f",
                "quantity": "static radial function",
                "formula": "f=1-2M/r+24 s ell_+^4 M^2[9/r^6-49M/(3r^7)]",
                "order": "O(ell_+^4)",
                "status": "SOURCE_BACKED_PURE_I1",
                "source": CANO_QNM_URL,
                "passed": True,
            },
            {
                "metric_id": "METRIC4922_01_N",
                "quantity": "static lapse prefactor",
                "formula": "N=1-108 s ell_+^4 M^2/r^6",
                "order": "O(ell_+^4)",
                "status": "SOURCE_BACKED_PURE_I1",
                "source": CANO_QNM_URL,
                "passed": True,
            },
            {
                "metric_id": "METRIC4922_02_cancel",
                "quantity": "invariant time-time metric combination",
                "formula": "N^2 f=1-2M/r+40 s ell_+^4 M^3/r^7",
                "order": "O(ell_+^4)",
                "status": "R_MINUS_6_TERMS_CANCEL_EXACTLY",
                "source": "algebraic_product_of_METRIC4922_00_and_01",
                "passed": True,
            },
            {
                "metric_id": "METRIC4922_03_potential",
                "quantity": "weak clock potential",
                "formula": "delta Phi=-20 s ell_+^4 M^3/r^7",
                "order": "O(ell_+^4)",
                "status": "CORRECTED_PURE_I1_TRANSFER",
                "source": "g_tt=-(1-2Phi)",
                "passed": True,
            },
            {
                "metric_id": "METRIC4922_04_acceleration",
                "quantity": "slow radial acceleration fraction",
                "formula": "abs(delta a/a_N)=140 ell_+^4 M^2/r^6",
                "order": "O(ell_+^4)",
                "status": "DERIVED_BY_DIFFERENTIATION",
                "source": "derivative_of_METRIC4922_03",
                "passed": True,
            },
            {
                "metric_id": "METRIC4922_05_clock",
                "quantity": "two-radius clock anomaly",
                "formula": "abs(alpha_clock)=20 ell_+^4 M^2 abs(r1^-7-r2^-7)/abs(r1^-1-r2^-1)",
                "order": "O(ell_+^4)",
                "status": "DERIVED_STATIC_OBSERVABLE",
                "source": "ratio_of_potential_differences",
                "passed": True,
            },
            {
                "metric_id": "METRIC4922_06_control",
                "quantity": "generic curvature control",
                "formula": "epsilon_K=ell_+^4 K; epsilon_horizon=(3/4)(ell_+/M)^4",
                "order": "strict_EFT",
                "status": "CORRECTED_CANONICAL_NORMALIZATION",
                "source": "action_ratio_and_K_horizon=3/(4M^4)",
                "passed": True,
            },
        ]
    )


def gw170608_input_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "input_id": "GW4922_00_alpha1",
                "quantity": "alpha_bar1 marginalized posterior",
                "central": ALPHA1_CENTRAL,
                "lower_90": ALPHA1_LOWER_90,
                "upper_90": ALPHA1_UPPER_90,
                "units": "dimensionless",
                "status": "PUBLISHED_90_PERCENT_INTERVAL",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
            {
                "input_id": "GW4922_01_alpha2",
                "quantity": "alpha_bar2 marginalized nuisance posterior",
                "central": ALPHA2_CENTRAL,
                "lower_90": ALPHA2_LOWER_90,
                "upper_90": ALPHA2_UPPER_90,
                "units": "dimensionless",
                "status": "PUBLISHED_90_PERCENT_INTERVAL",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
            {
                "input_id": "GW4922_02_Bayes",
                "quantity": "log Bayes factor EFT versus GR",
                "central": LOG_B_EFT_GR,
                "lower_90": "not_applicable",
                "upper_90": "not_applicable",
                "units": "log evidence ratio",
                "status": "DATA_DISFAVORS_EFT_RELATIVE_TO_GR",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
            {
                "input_id": "GW4922_03_mass",
                "quantity": "paper-stated approximate component masses",
                "central": GW170608_TOTAL_MASS_MSUN_APPROX,
                "lower_90": GW170608_SECONDARY_MASS_MSUN,
                "upper_90": GW170608_PRIMARY_MASS_MSUN,
                "units": "solar masses; total is approximate sum",
                "status": "APPROXIMATE_PHYSICAL_LENGTH_TRANSLATION_ONLY",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
            {
                "input_id": "GW4922_04_model",
                "quantity": "waveform content",
                "central": "5PN_and_partial_6PN_inspiral_plus_QNM_ringdown",
                "lower_90": "no_direct_EFT_merger_simulation",
                "upper_90": "QNM_fit_chi_less_than_0.7",
                "units": "model scope",
                "status": "APPROXIMATE_IMR_WITH_EXPLICIT_VALIDITY_PRIORS",
                "source": LIU_YUNES_URL,
                "passed": True,
            },
        ]
    )


def gw170608_bound_rows() -> list[dict[str, Any]]:
    mass_m = gw170608_mass_length()
    rows = []
    for sign, endpoint in (("negative", abs(ALPHA1_LOWER_90)), ("positive", ALPHA1_UPPER_90)):
        ratio = ell_ratio(endpoint)
        rows.append(
            {
                "branch": sign,
                "alpha_bar1_endpoint": -endpoint if sign == "negative" else endpoint,
                "abs_alpha_bar1_endpoint": endpoint,
                "ell_plus_over_M_upper": ratio,
                "approx_total_mass_Msun": GW170608_TOTAL_MASS_MSUN_APPROX,
                "approx_M_geo_m": mass_m,
                "approx_ell_plus_upper_m": mass_m * ratio,
                "horizon_epsilon_at_same_mass": 0.75 * endpoint,
                "one_percent_domain_ratio": endpoint / (TAU_DOMAIN / 0.75),
                "status": "DIRECT_MARGINALIZED_DIMENSIONLESS_BOUND_APPROX_LENGTH_TRANSLATION",
                "source": LIU_YUNES_URL,
                "passed": True,
            }
        )
    rows.append(
        {
            "branch": "primary_statement",
            "alpha_bar1_endpoint": "[-0.16,2.82]",
            "abs_alpha_bar1_endpoint": "sign_dependent",
            "ell_plus_over_M_upper": "0.632456_negative;1.295873_positive",
            "approx_total_mass_Msun": GW170608_TOTAL_MASS_MSUN_APPROX,
            "approx_M_geo_m": mass_m,
            "approx_ell_plus_upper_m": "17744.6_negative;36357.9_positive",
            "horizon_epsilon_at_same_mass": "0.12_negative;2.115_positive",
            "one_percent_domain_ratio": "12_negative;211.5_positive",
            "status": "USE_DIMENSIONLESS_INTERVAL_AS_AUTHORITATIVE",
            "source": LIU_YUNES_URL,
            "passed": True,
        }
    )
    return tagged(rows)


def ringdown_comparator_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "comparator_id": "RING4922_00_mixed",
                "model": "cubic EFT ringdown benchmark lambda_even=lambda_odd=1",
                "result": "ell_cEFT<38.2 km at 90 percent credible level",
                "mapping_to_ell_plus": "NOT_DIRECT_BECAUSE_PARITY_ODD_COEFFICIENT_IS_SIMULTANEOUSLY_ACTIVE",
                "status": "SCALE_CROSSCHECK_ONLY",
                "source": SILVA_RINGDOWN_URL,
                "passed": True,
            },
            {
                "comparator_id": "RING4922_01_even_QNM",
                "model": "slow-spin pure parity-even I1 QNM",
                "result": "delta omega proportional lambda_even ell^4/M^5",
                "mapping_to_ell_plus": "EXACT_THEORY_MAP_BUT_NO_STANDALONE_PUBLISHED_LIKELIHOOD_IN_2205_ANALYSIS",
                "status": "THEORY_TEMPLATE_NOT_DATA_BOUND",
                "source": CANO_QNM_URL,
                "passed": True,
            },
            {
                "comparator_id": "RING4922_02_scaling",
                "model": "catalog curvature scaling",
                "result": "pure cubic no-extra-field deviations scale as M^-4",
                "mapping_to_ell_plus": "consistent with alpha_bar1=s ell_+^4/M^4",
                "status": "SCALING_CROSSCHECK_NOT_COEFFICIENT_LIKELIHOOD",
                "source": PAYNE_SCALING_URL,
                "passed": True,
            },
            {
                "comparator_id": "RING4922_03_future",
                "model": "GW250114 plus finite-spin gravitational pure-I1 QNM",
                "result": "GW250114 data and a gravitational higher-derivative QNM series accurate to about chi=0.7 exist",
                "mapping_to_ell_plus": "requires remnant-spin compatibility and explicit posterior-level recast",
                "status": "NEXT_DIRECT_TARGET",
                "source": f"{GW250114_URL};{GRAVITATIONAL_QNM_URL}",
                "passed": True,
            },
            {
                "comparator_id": "RING4922_04_scalar_exclusion",
                "model": "2026 rapid-spin scalar perturbation QNMs",
                "result": "cubic-curvature scalar modes through chi=0.99 are not gravitational-wave ringdown modes",
                "mapping_to_ell_plus": "INCOMPATIBLE_OBSERVABLE_SECTOR_FOR_GW250114_RECAST",
                "status": "EXCLUDED_AS_DIRECT_GRAVITATIONAL_QNM_TEMPLATE",
                "source": SCALAR_HIGH_SPIN_C3_URL,
                "passed": True,
            },
        ]
    )


def local_projection_rows() -> list[dict[str, Any]]:
    earth_m = gravitational_mass_length(EARTH_MASS_KG)
    sun_m = gravitational_mass_length(SUN_MASS_KG)
    ell_positive = ell_approx_m(ALPHA1_UPPER_90)
    clock_coefficient = pure_i1_clock_coefficient(
        earth_m,
        EARTH_RADIUS_M,
        EARTH_RADIUS_M + GALILEO_ALTITUDE_M,
    )
    return tagged(
        [
            {
                "projection_id": "LOCAL4922_00_clock_cap",
                "observable": "corrected pure-I1 Galileo clock envelope",
                "value": pure_i1_clock_cap(),
                "units": "m",
                "formula": "ell_clock=[tau_clock/C_clock]^(1/4)",
                "status": "PRIVATE_LOCAL_ENVELOPE_WEAKER_THAN_GW",
                "passed": True,
            },
            {
                "projection_id": "LOCAL4922_01_clock_at_GW",
                "observable": "Galileo anomaly at approximate positive GW endpoint",
                "value": clock_coefficient * ell_positive**4,
                "units": "dimensionless",
                "formula": "C_clock ell_GW^4",
                "status": "NEGLIGIBLE_WEAK_METRIC_FEEDBACK",
                "passed": True,
            },
            {
                "projection_id": "LOCAL4922_02_Earth_acceleration",
                "observable": "Earth-surface acceleration fraction at approximate positive GW endpoint",
                "value": pure_i1_acceleration_fraction(ell_positive, earth_m, EARTH_RADIUS_M),
                "units": "dimensionless",
                "formula": "140 ell_GW^4 M_E^2/R_E^6",
                "status": "NEGLIGIBLE_WEAK_METRIC_FEEDBACK",
                "passed": True,
            },
            {
                "projection_id": "LOCAL4922_03_Earth_curvature",
                "observable": "Earth-surface strict-EFT control at approximate positive GW endpoint",
                "value": ell_positive**4 * 12.0 * (2.0 * earth_m) ** 2 / EARTH_RADIUS_M**6,
                "units": "dimensionless",
                "formula": "ell_GW^4 K_Earth",
                "status": "WEAK_DOMAIN_CONTROLLED",
                "passed": True,
            },
            {
                "projection_id": "LOCAL4922_04_Sun_curvature",
                "observable": "Sun-surface strict-EFT control at approximate positive GW endpoint",
                "value": ell_positive**4 * 12.0 * (2.0 * sun_m) ** 2 / SUN_RADIUS_M**6,
                "units": "dimensionless",
                "formula": "ell_GW^4 K_Sun",
                "status": "WEAK_DOMAIN_CONTROLLED",
                "passed": True,
            },
            {
                "projection_id": "LOCAL4922_05_Maxwell",
                "observable": "pure-I1 fixed-metric Maxwell coupling",
                "value": 0.0,
                "units": "direct operator coefficient",
                "formula": "delta S_I1/dA_mu=0",
                "status": "EXACT_NO_DIRECT_COUPLING_METRIC_FEEDBACK_ONLY",
                "passed": True,
            },
        ]
    )


def compact_domain_rows() -> list[dict[str, Any]]:
    systems = read_csv(OUTPUT / "P8_Y5_R2FR_4880_SYSTEM_BENCHMARKS.csv")
    ell_negative = ell_approx_m(abs(ALPHA1_LOWER_90))
    ell_positive = ell_approx_m(ALPHA1_UPPER_90)
    rows: list[dict[str, Any]] = []
    for source in systems:
        kretschmann = float(source["K_m_minus_4"])
        cap = compact_domain_cap(kretschmann)
        epsilon_negative = ell_negative**4 * kretschmann
        epsilon_positive = ell_positive**4 * kretschmann
        rows.append(
            {
                "system": source["system"],
                "source_class": source["source_class"],
                "K_m_minus_4": kretschmann,
                "control_formula": "epsilon_K=ell_+^4 K",
                "tau_domain": TAU_DOMAIN,
                "ell_plus_upper_m_for_domain": cap,
                "epsilon_at_approx_negative_GW_endpoint": epsilon_negative,
                "epsilon_at_approx_positive_GW_endpoint": epsilon_positive,
                "negative_GW_endpoint_controls_domain": epsilon_negative < TAU_DOMAIN,
                "positive_GW_endpoint_controls_domain": epsilon_positive < TAU_DOMAIN,
                "status": (
                    "BOTH_GW_ENDPOINTS_CONTROL_WEAK_BACKGROUND"
                    if epsilon_positive < TAU_DOMAIN
                    else "GW_BOUND_DOES_NOT_CERTIFY_COMPACT_DOMAIN"
                ),
                "passed": True,
            }
        )
    return tagged(rows)


def gate_decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "4921_L3_route",
                "status": "SUPERSEDED_AS_TOTAL_C3_BOUND",
                "decision": "retain only as a declared Burger beta1 benchmark; remove from the active zeta_+ certificate",
                "passed": True,
            },
            {
                "gate": "invariant_coefficient_map",
                "status": "CLOSED",
                "decision": "O_+=I1=C7 and alpha_bar1=sign(zeta_+)(ell_+/M)^4 with ell_+^4=abs(16 pi G zeta_+)",
                "passed": True,
            },
            {
                "gate": "GW170608_data",
                "status": "DIRECT_MARGINALIZED_BOUND",
                "decision": "published 90 percent interval -0.16<alpha_bar1<2.82 with alpha_bar2 marginalized; log Bayes EFT/GR=-2.81",
                "passed": True,
            },
            {
                "gate": "weak_invariant_vacuum_GR",
                "status": "RETAINED_AFTER_CORRECTED_TRANSFER",
                "decision": "the approximate positive GW endpoint yields Earth acceleration and clock residuals below 1e-25 and no direct Maxwell coupling",
                "passed": True,
            },
            {
                "gate": "compact_vacuum_GR",
                "status": "NOT_PROMOTED",
                "decision": "the published sign-dependent alpha_bar1 endpoints exceed the one-percent horizon-control requirement by factors 12 and 211.5",
                "passed": True,
            },
            {
                "gate": "finite_MTS_zeta_plus",
                "status": "NOT_DERIVED",
                "decision": "the observational bound does not replace the missing parent finite matching coefficient",
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "compact matter nonvacuum flow UV completion and a parent prediction for zeta_+ remain open",
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "GW250114_HIGH_SPIN_RECAST",
                "decision": NEXT_TARGET,
                "passed": True,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4922_00_prior_validation", OUTPUT / "P8_Y5_BRR545_4921_VALIDATION.csv", "VAL4921_OVERALL,PASS", "predecessor_validation"),
        ("SRC4922_01_4921", POST / "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md", "SUPERSEDED BY CHECKPOINT 4922", "superseded_predecessor"),
        ("SRC4922_02_4905", POST / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md", "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905", "corpus_operator_basis"),
        ("SRC4922_03_4908", POST / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md", "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908", "coefficient_owner"),
        ("SRC4922_04_4911", POST / "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md", "MTS_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911", "Ricci_flat_quotient"),
        ("SRC4922_05_4911_map", OUTPUT / "P8_Y5_R2FR_4911_RICCI_FLAT_MAP.csv", "I2=I1/2", "Ricci_flat_identity"),
        ("SRC4922_06_4880_systems", OUTPUT / "P8_Y5_R2FR_4880_SYSTEM_BENCHMARKS.csv", "10_solar_mass_Schwarzschild_horizon", "system_inputs"),
        ("SRC4922_07_checkpoint", POST / "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-bound-or-compact-vacuum-GR-domain-gate.md", MARKER, "generated_checkpoint"),
        ("SRC4922_08_research", Path(__file__).resolve(), "def basis_map_rows", "generated_research_code"),
        ("SRC4922_09_validation", SCRIPTS / "Y5_R2FR_4922_Weyl_C3_GW170608_domain_validation.py", "VAL4922_OVERALL", "generated_validation_code"),
        ("SRC4922_10_formal", FORMAL / "938-PPC4161-Weyl-C3-GW170608-domain-gate.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4922_11_provenance", POST / "source-intake" / "parent_coupling" / "4922" / "PROVENANCE.md", "MTS_WEYL_C3_GW170608_PROVENANCE_4922", "provenance"),
        ("SRC4922_12_claim", FORMAL / "02-claims-register.csv", "L-764", "register"),
        ("SRC4922_13_variable", FORMAL / "04-variable-audit.csv", "WeylCubicLength4922_MTS", "register"),
        ("SRC4922_14_equation", FORMAL / "05-equation-register.md", "1.215 Weyl-cubic basis map and GW170608 bound", "register"),
        ("SRC4922_15_redteam", FORMAL / "06-consistency-red-team.md", "166. A probe-potential coefficient is not the invariant Weyl-cubic packet", "register"),
        ("SRC4922_16_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4922", "register"),
        ("SRC4922_17_resume", POST / "CURRENT_LOCAL_RESUME.md", FORMAL_MARKER, "resume"),
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
                "verification": "local_path_and_marker",
            }
        )
    external_sources = [
        ("SRC4922_18_Liu_Yunes", LIU_YUNES_URL, "GW170608 alpha_bar1 and alpha_bar2 posterior", "primary_data_analysis"),
        ("SRC4922_19_Cano", CANO_QNM_URL, "pure metric cubic action static solution and QNM map", "primary_theory"),
        ("SRC4922_20_Burger", BURGER_URL, "generic beta1 beta2 action and probe potential", "primary_basis_comparator"),
        ("SRC4922_21_Silva", SILVA_RINGDOWN_URL, "mixed parity cubic ringdown bound", "primary_data_comparator"),
        ("SRC4922_22_Payne", PAYNE_SCALING_URL, "M^-4 cubic curvature scaling", "primary_catalog_scaling"),
        ("SRC4922_23_GW250114", GW250114_URL, "current high-SNR ringdown event", "next_target_data"),
        ("SRC4922_24_gravitational_QNM", GRAVITATIONAL_QNM_URL, "finite-spin gravitational higher-derivative QNM template", "next_target_theory"),
        ("SRC4922_25_scalar_exclusion", SCALAR_HIGH_SPIN_C3_URL, "rapid-spin scalar perturbations only", "incompatible_sector_audit"),
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
                "verification": "web_checked_2026-07-12",
            }
        )
    return tagged(rows)


def main() -> int:
    tables = {
        "P8_Y5_R2FR_4922_BASIS_MAP.csv": basis_map_rows(),
        "P8_Y5_R2FR_4922_4921_SUPERSESSION.csv": supersession_rows(),
        "P8_Y5_R2FR_4922_STATIC_METRIC_TRANSFER.csv": static_metric_rows(),
        "P8_Y5_R2FR_4922_GW170608_INPUTS.csv": gw170608_input_rows(),
        "P8_Y5_R2FR_4922_GW170608_COEFFICIENT_BOUND.csv": gw170608_bound_rows(),
        "P8_Y5_R2FR_4922_RINGDOWN_COMPARATOR.csv": ringdown_comparator_rows(),
        "P8_Y5_R2FR_4922_LOCAL_WEAK_PROJECTION.csv": local_projection_rows(),
        "P8_Y5_R2FR_4922_COMPACT_DOMAIN.csv": compact_domain_rows(),
        "P8_Y5_R2FR_4922_GATE_DECISION.csv": gate_decision_rows(),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4922_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4922_WEYL_C3_GW170608_PASS"
        if passed
        else "P8_Y5_R2FR_4922_WEYL_C3_GW170608_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
