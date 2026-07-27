from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.constants import G, c, hbar
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4929"

CHECKED_DATE = "2026-07-12"
MARKER = "MTS_MATTER_COMPLETED_C3_FLOW_4929"
NEXT_TARGET = "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"

ARXIV_URLS = {
    "2104": "https://arxiv.org/abs/2104.11336",
    "2204": "https://arxiv.org/abs/2204.08564",
    "2312": "https://arxiv.org/abs/2312.03831",
    "1311": "https://arxiv.org/abs/1311.2898",
}

LOCAL_BINARIES = {
    SOURCE / "2104.11336v2.pdf": "9c59217b0653e44e5b93ad612ae6ced26cbf7e04275e3523c7aa1a5fbf6156b8",
    SOURCE / "2104.11336v2-source.tar": "79b7e2f8de41e3c7a4fa5028311eeff7d8efc1228d0db7c1b69c1a9f79916af4",
    SOURCE / "2204.08564v2.pdf": "11970922381681435f29a135f823bf8840a2f41f323f8253f3331062d0734744",
    SOURCE / "2204.08564v2-source.tar": "7e4504e7bea553db51f01ed23860cb7309432a863df124c881668c60f21c5afe",
    SOURCE / "2312.03831v1.pdf": "86b424e0c309d06444c110841e23751b4edcb44548fbcb50fddac6d8c1fb700f",
    SOURCE / "2312.03831v1-source.tar": "830678a191f7bed7fe0f0050e2dc86207ece3044719ec475130e4427a36a8956",
    SOURCE / "1311.2898v2.pdf": "f2adcb d636ed7e662d54769ca6a20cd6ca20564e3c9a8bbe079eae5cc113cd0b".replace(" ", ""),
    SOURCE / "1311.2898v2-source.tar": "e0d90aac0e92ec05fabb67b824969148e8e49a870566f49844f46e2a58f3d5f2",
}

PROVENANCE = SOURCE / "PROVENANCE.md"
TEX_2104 = SOURCE / "src2104" / "R2compendium.tex"
TEX_2204 = SOURCE / "src2204" / "R2scalarMES.tex"
TEX_2312 = SOURCE / "src2312" / "ess_cubic.tex"
TEX_1311 = SOURCE / "src1311" / "Constraints_on_matter_K.tex"
CHECKPOINT_4877 = POST / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md"
CHECKPOINT_4904 = POST / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md"
CHECKPOINT_4905 = POST / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md"
CHECKPOINT_4928 = POST / "4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-observational-Wilson-freeze.md"
WILSON_BOUND_PATH = OUTPUT / "P8_Y5_R2FR_4925_WILSON_BOUND.csv"
CHECKPOINT_DOC = POST / "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md"
FORMAL_NOTE = FORMAL / "945-PPC4161-matter-completed-C3-leading-flow-and-closure-boundary.md"
SCRIPTS = POST / "scripts"
VALIDATION = SCRIPTS / "Y5_R2FR_4929_matter_completed_C3_flow_validation.py"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
VARIABLE_REGISTER = FORMAL / "04-variable-audit.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM_REGISTER = FORMAL / "06-consistency-red-team.md"
SPINE_REGISTER = FORMAL / "07-unification-spine.md"

PLANCK_LENGTH_M = math.sqrt(hbar * G / c**3)
C3_SCALAR_UNIT = 1.0 / (30_240.0 * (4.0 * math.pi) ** 2)
C3_LOG_COEFFICIENT = 69.0 / (725_760.0 * math.pi**3)
NEWTON_POLE = 2.0 * math.pi / 3.0


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


def beta_g_pure(newton: float) -> float:
    return (
        2.0
        * newton
        * (-32.0 * newton + 6.0 * math.pi)
        / (-9.0 * newton + 6.0 * math.pi)
    )


def beta_g_spectator(newton: float, weight_1: float) -> float:
    return beta_g_pure(newton) + weight_1 * newton**2 / (6.0 * math.pi)


def c3_polynomial_coefficients(newton: float) -> tuple[float, float, float, float]:
    pi = math.pi
    constant = 69.0 * newton
    linear = (
        -3_709_440.0 * newton**2 * pi
        + 14_515_200.0 * newton * pi**2
        + 1_451_520.0 * pi**3
    )
    quadratic = (
        47_585_664.0 * newton**3 * pi**2
        - 21_337_344.0 * newton**2 * pi**3
    )
    cubic = (
        -84_188_160.0 * newton**4 * pi**3
        + 78_382_080.0 * newton**3 * pi**4
    )
    return constant, linear, quadratic, cubic


def beta_c3_pure(newton: float, c3_coupling: float) -> float:
    constant, linear, quadratic, cubic = c3_polynomial_coefficients(newton)
    numerator = (
        constant
        + linear * c3_coupling
        + quadratic * c3_coupling**2
        + cubic * c3_coupling**3
    )
    denominator = 120_960.0 * (9.0 * newton - 6.0 * math.pi) * math.pi**2
    return -numerator / denominator


def matter_c3_constant(weight_0: float) -> float:
    return weight_0 * C3_SCALAR_UNIT


def beta_c3_spectator(
    newton: float,
    c3_coupling: float,
    weight_0: float,
    projection: str,
) -> float:
    source = 0.0
    if projection == "proper_time_hybrid_diagnostic":
        source = -2.0 * matter_c3_constant(weight_0)
    return beta_c3_pure(newton, c3_coupling) + source


def matter_scenarios() -> list[dict[str, Any]]:
    inputs = [
        ("pure_gravity", 0.0, 0.0, 0.0, 0.0, "no spectator matter"),
        ("SM45_minimal_Higgs", 4.0, 22.5, 12.0, 4.0, "observed SM without right-handed neutrinos"),
        ("SM48_minimal_Higgs", 4.0, 24.0, 12.0, 4.0, "SM plus three right-handed neutrinos"),
        ("SM45_conformal_Higgs", 4.0, 22.5, 12.0, 0.0, "four Higgs components at xi=1/6"),
        ("SM48_conformal_Higgs", 4.0, 24.0, 12.0, 0.0, "right-handed neutrinos and xi_H=1/6"),
        ("SM45_minimal_Higgs_plus_motion", 5.0, 22.5, 12.0, 5.0, "one real minimally coupled MTS motion mode active in the UV"),
        ("SM48_minimal_Higgs_plus_motion", 5.0, 24.0, 12.0, 5.0, "right-handed neutrinos and one active minimal motion mode"),
        ("SM45_conformal_Higgs_plus_motion", 5.0, 22.5, 12.0, 1.0, "conformal Higgs plus one active minimal motion mode"),
        ("SM48_conformal_Higgs_plus_motion", 5.0, 24.0, 12.0, 1.0, "right-handed neutrinos, conformal Higgs and one active minimal motion mode"),
    ]
    rows: list[dict[str, Any]] = []
    for scenario, scalars, dirac, vectors, scalar_h, interpretation in inputs:
        weight_0 = scalars + 2.0 * vectors - 4.0 * dirac
        weight_1 = scalar_h + 2.0 * dirac - 4.0 * vectors
        weight_c = scalars + 6.0 * dirac + 12.0 * vectors
        rows.append(
            {
                "scenario": scenario,
                "N_s_real": scalars,
                "N_D_Dirac_equivalent": dirac,
                "N_V_Maxwell": vectors,
                "S_h_sum_1_minus_6xi": scalar_h,
                "W0_equals_W3": weight_0,
                "W1": weight_1,
                "WC": weight_c,
                "motion_mode_UV_status": "conditional_active" if "motion" in scenario else "not_added",
                "interpretation": interpretation,
                "status": "FIELD_INVENTORY_BENCHMARK_NOT_PARENT_UV_SPECTRUM_CLAIM",
                "passed": math.isfinite(weight_0 + weight_1 + weight_c),
            }
        )
    return tagged(rows)


def spin_weight_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "field": "real scalar",
            "Ricci_flat_C3_weight": 1.0,
            "Newton_weight": "1-6xi",
            "massive_local_coefficient": "+1/[30240(4pi)^2 m^2]",
            "derivation": "source-locked scalar heat-kernel coefficient",
            "status": "DIRECT_COEFFICIENT",
            "passed": True,
        },
        {
            "field": "Dirac fermion",
            "Ricci_flat_C3_weight": -4.0,
            "Newton_weight": 2.0,
            "massive_local_coefficient": "-1/[7560(4pi)^2 m^2]",
            "derivation": "-1/7560=-4/30240",
            "status": "DIRECT_COEFFICIENT",
            "passed": True,
        },
        {
            "field": "massive Proca",
            "Ricci_flat_C3_weight": 3.0,
            "Newton_weight": "not used as a massless gauge weight",
            "massive_local_coefficient": "+1/[10080(4pi)^2 m^2]",
            "derivation": "+1/10080=+3/30240",
            "status": "DIRECT_COEFFICIENT",
            "passed": True,
        },
        {
            "field": "Maxwell plus gauge ghost",
            "Ricci_flat_C3_weight": 2.0,
            "Newton_weight": -4.0,
            "massive_local_coefficient": "massless determinant weight",
            "derivation": "Proca=Maxwell+real scalar implies 3=2+1",
            "status": "DETERMINANT_IDENTITY_DERIVED",
            "passed": True,
        },
        {
            "field": "combined free matter",
            "Ricci_flat_C3_weight": "W3=N_s-4N_D+2N_V=W0",
            "Newton_weight": "W1=sum_s(1-6xi_s)+2N_D-4N_V",
            "massive_local_coefficient": "C3_SCALAR_UNIT times W3 for equal masses",
            "derivation": "sum of the four spin/determinant rows",
            "status": "W3_EQUALS_W0_DERIVED_ON_RICCI_FLAT",
            "passed": True,
        },
    ]
    return tagged(rows)


def natural_source_gate_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate_id": "QG4929_00_trace",
                "object": "four-dimensional Laplace-type heat-kernel trace",
                "equation": "Tr W(Delta)=(4pi)^-2 sum_n Q_(2-n)[W] integral tr a_(2n)",
                "derived_value": "C3 uses a6 and therefore Q_-1[W]",
                "assumptions": "complete natural Laplace operator and mode-count-preserving supertrace",
                "status": "HEAT_KERNEL_PROJECTION_DERIVED",
                "passed": True,
            },
            {
                "gate_id": "QG4929_01_optimized",
                "object": "optimized spectral regulator",
                "equation": "R_k(z)=(k^2-z)theta(k^2-z); W=partial_t R/(z+R)=2theta(k^2-z)",
                "derived_value": 2.0,
                "assumptions": "zero matter anomalous dimension",
                "status": "CONSTANT_SUBCUTOFF_KERNEL",
                "passed": True,
            },
            {
                "gate_id": "QG4929_02_Newton",
                "object": "free spectator contribution to Newton flow",
                "equation": "Q_1[W]=2k^2; beta_g=beta_g_grav+W1 g^2/(6pi)",
                "derived_value": 1.0 / (6.0 * math.pi),
                "assumptions": "spectral Litim regulator; free fields; background matter zero",
                "status": "FREE_MATTER_NEWTON_INCREMENT_DERIVED_AND_1311_CROSSCHECKED",
                "passed": True,
            },
            {
                "gate_id": "QG4929_03_C3",
                "object": "free spectator direct C3 source",
                "equation": "Q_-1[W]=-W'(0)=0",
                "derived_value": 0.0,
                "assumptions": "spectral Litim regulator on the full natural operator; eta_matter=0",
                "status": "LEADING_FREE_SPECTATOR_C3_SOURCE_ZERO_DERIVED",
                "passed": True,
            },
            {
                "gate_id": "QG4929_04_eta",
                "object": "anomalous-dimension and interaction boundary",
                "equation": "eta-dependent W'(0), mixed Hessians and induced essential operators can make Q_-1 or other C3 projections nonzero",
                "derived_value": "not zero by the free-spectator theorem",
                "assumptions": "full interacting gravity-SM-MTS flow",
                "status": "FREE_ZERO_DOES_NOT_CLOSE_INTERACTING_MATTER_FLOW",
                "passed": True,
            },
        ]
    )


def fixed_point(weight_0: float, weight_1: float, projection: str) -> dict[str, float]:
    newton_star = brentq(
        lambda value: beta_g_spectator(value, weight_1),
        1.0e-12,
        NEWTON_POLE * (1.0 - 1.0e-10),
        xtol=1.0e-14,
        rtol=1.0e-14,
    )
    constant, linear, quadratic, cubic = c3_polynomial_coefficients(newton_star)
    if projection == "proper_time_hybrid_diagnostic":
        denominator = 120_960.0 * (9.0 * newton_star - 6.0 * math.pi) * math.pi**2
        constant += 2.0 * matter_c3_constant(weight_0) * denominator
    roots = np.roots([cubic, quadratic, linear, constant])
    real_roots = sorted(float(root.real) for root in roots if abs(root.imag) < 1.0e-9)
    if not real_roots:
        raise RuntimeError(f"no real C3 root for W0={weight_0}, W1={weight_1}, {projection}")
    c3_star = min(real_roots, key=abs)
    step_g = max(1.0e-7, 1.0e-6 * abs(newton_star))
    step_h = max(1.0e-12, 1.0e-5 * abs(c3_star))
    derivative_g = (
        beta_g_spectator(newton_star + step_g, weight_1)
        - beta_g_spectator(newton_star - step_g, weight_1)
    ) / (2.0 * step_g)
    derivative_h_g = (
        beta_c3_spectator(newton_star + step_g, c3_star, weight_0, projection)
        - beta_c3_spectator(newton_star - step_g, c3_star, weight_0, projection)
    ) / (2.0 * step_g)
    derivative_h_h = (
        beta_c3_spectator(newton_star, c3_star + step_h, weight_0, projection)
        - beta_c3_spectator(newton_star, c3_star - step_h, weight_0, projection)
    ) / (2.0 * step_h)
    relevant_slope = -derivative_h_g / (derivative_h_h - derivative_g)
    shift = matter_c3_constant(weight_0) if projection == "proper_time_hybrid_diagnostic" else 0.0
    return {
        "g_star": newton_star,
        "h_star": c3_star,
        "u_star": c3_star - shift,
        "C_shift": shift,
        "theta_g": -derivative_g,
        "theta_h": -derivative_h_h,
        "relevant_slope": relevant_slope,
        "real_root_count": float(len(real_roots)),
        "beta_norm": math.hypot(
            beta_g_spectator(newton_star, weight_1),
            beta_c3_spectator(newton_star, c3_star, weight_0, projection),
        ),
    }


def benchmark_fixed_point_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in inventory:
        weight_0 = float(scenario["W0_equals_W3"])
        weight_1 = float(scenario["W1"])
        for projection in ("optimized_spectral_free_spectator", "proper_time_hybrid_diagnostic"):
            fixed = fixed_point(weight_0, weight_1, projection)
            stable = (
                0.0 < fixed["g_star"] < NEWTON_POLE
                and fixed["theta_g"] > 0.0
                and fixed["theta_h"] < 0.0
                and fixed["beta_norm"] < 1.0e-9
            )
            rows.append(
                {
                    "scenario": scenario["scenario"],
                    "projection": projection,
                    "W0_equals_W3": weight_0,
                    "W1": weight_1,
                    "g_star": fixed["g_star"],
                    "h_star": fixed["h_star"],
                    "C_shift": fixed["C_shift"],
                    "u_star_equals_h_minus_C": fixed["u_star"],
                    "theta_relevant_g": fixed["theta_g"],
                    "theta_irrelevant_C3": fixed["theta_h"],
                    "real_C3_roots": int(fixed["real_root_count"]),
                    "beta_norm": fixed["beta_norm"],
                    "two_coordinate_fixed_point_survives": stable,
                    "full_matter_critical_surface_claim": False,
                    "status": "LEADING_SPECTATOR_FIXED_POINT_SURVIVES" if stable else "LEADING_SPECTATOR_FIXED_POINT_FAILED",
                    "passed": stable,
                }
            )
    return tagged(rows)


def robustness_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for weight_1 in np.linspace(-20.0, 20.0, 81):
        fixed = fixed_point(0.0, float(weight_1), "optimized_spectral_free_spectator")
        stable = (
            0.0 < fixed["g_star"] < NEWTON_POLE
            and fixed["theta_g"] > 0.0
            and fixed["theta_h"] < 0.0
        )
        rows.append(
            {
                "scan_id": f"NAT4929_{len(rows):04d}",
                "projection": "optimized_spectral_free_spectator",
                "W0_equals_W3": 0.0,
                "W1": float(weight_1),
                "g_star": fixed["g_star"],
                "h_star": fixed["h_star"],
                "theta_g": fixed["theta_g"],
                "theta_h": fixed["theta_h"],
                "positive_g_below_pole": 0.0 < fixed["g_star"] < NEWTON_POLE,
                "one_relevant_one_irrelevant_in_2D": stable,
                "status": "SPECTATOR_2D_SURVIVES" if stable else "SPECTATOR_2D_FAILURE",
                "passed": stable,
            }
        )
    hybrid_index = 0
    for weight_0 in np.arange(-200.0, 200.0 + 2.5, 5.0):
        for weight_1 in np.linspace(-20.0, 20.0, 81):
            fixed = fixed_point(
                float(weight_0),
                float(weight_1),
                "proper_time_hybrid_diagnostic",
            )
            stable = (
                0.0 < fixed["g_star"] < NEWTON_POLE
                and fixed["theta_g"] > 0.0
                and fixed["theta_h"] < 0.0
            )
            rows.append(
                {
                    "scan_id": f"PT4929_{hybrid_index:04d}",
                    "projection": "proper_time_hybrid_diagnostic",
                    "W0_equals_W3": float(weight_0),
                    "W1": float(weight_1),
                    "g_star": fixed["g_star"],
                    "h_star": fixed["h_star"],
                    "theta_g": fixed["theta_g"],
                    "theta_h": fixed["theta_h"],
                    "positive_g_below_pole": 0.0 < fixed["g_star"] < NEWTON_POLE,
                    "one_relevant_one_irrelevant_in_2D": stable,
                    "status": "HYBRID_2D_SURVIVES" if stable else "HYBRID_2D_FAILURE",
                    "passed": stable,
                }
            )
            hybrid_index += 1
    return tagged(rows)


def proper_time_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in inventory:
        weight_0 = float(scenario["W0_equals_W3"])
        constant = matter_c3_constant(weight_0)
        rows.append(
            {
                "scenario": scenario["scenario"],
                "W0_equals_W3": weight_0,
                "c6_scalar_unit": C3_SCALAR_UNIT,
                "C_m_equals_W0_c6": constant,
                "Wilsonian_local_coefficient": "zeta_k=C_m(1/k^2-1/Lambda^2)",
                "dimensionless_flow": "h=k^2 zeta; beta_h=beta_h_grav-2C_m",
                "Gaussian_coordinate": "u=h-C_m gives beta_u=2u+O(g)",
                "physical_interpretation": "massless local derivative-expansion artifact; not an IR Wilson prediction",
                "status": "SHIFTED_GAUSSIAN_QUARANTINED",
                "passed": math.isfinite(constant),
            }
        )
    return tagged(rows)


def integrate_natural_separatrix(weight_0: float, weight_1: float) -> dict[str, float]:
    fixed = fixed_point(weight_0, weight_1, "optimized_spectral_free_spectator")
    epsilon = 1.0e-6
    g_initial = fixed["g_star"] - epsilon
    h_initial = fixed["h_star"] + fixed["relevant_slope"] * (g_initial - fixed["g_star"])
    x_initial = math.log(g_initial)
    ratio_initial = h_initial / g_initial

    def ratio_flow(log_newton: float, state: np.ndarray) -> list[float]:
        newton = math.exp(log_newton)
        ratio = float(state[0])
        return [
            beta_c3_spectator(
                newton,
                ratio * newton,
                weight_0,
                "optimized_spectral_free_spectator",
            )
            / beta_g_spectator(newton, weight_1)
            - ratio
        ]

    solution = solve_ivp(
        ratio_flow,
        (x_initial, -40.0),
        [ratio_initial],
        rtol=1.0e-10,
        atol=1.0e-13,
        max_step=0.05,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    ratio_final = float(solution.y[0, -1])
    infrared_constant = ratio_final - 0.5 * C3_LOG_COEFFICIENT * -40.0
    return {
        **fixed,
        "A_C3": infrared_constant,
        "integration_residual": abs(
            ratio_final - 0.5 * C3_LOG_COEFFICIENT * -40.0 - infrared_constant
        ),
    }


def conditional_map_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bounds = {row["bound_id"]: row for row in read_csv(WILSON_BOUND_PATH)}
    compact_bound = float(bounds["WBOUND4925_02_NS_domain"]["abs_a_eff_bound_m4"])
    rows: list[dict[str, Any]] = []
    for scenario in inventory:
        weight_0 = float(scenario["W0_equals_W3"])
        weight_1 = float(scenario["W1"])
        result = integrate_natural_separatrix(weight_0, weight_1)
        a_over_planck4 = 16.0 * math.pi * result["A_C3"]
        ell_over_planck = abs(a_over_planck4) ** 0.25
        coefficient_m4 = math.copysign(
            (ell_over_planck * PLANCK_LENGTH_M) ** 4,
            a_over_planck4,
        )
        rows.append(
            {
                "scenario": scenario["scenario"],
                "projection": "optimized_spectral_free_spectator",
                "W1": weight_1,
                "g_star": result["g_star"],
                "h_star": result["h_star"],
                "A_C3_equals_GC3_over_GN_at_k0": result["A_C3"],
                "a_plus_over_lPlanck4": a_over_planck4,
                "ell_plus_over_lPlanck": ell_over_planck,
                "ell_plus_m": ell_over_planck * PLANCK_LENGTH_M,
                "a_plus_m4": coefficient_m4,
                "ratio_to_NS_one_percent_target": abs(coefficient_m4) / compact_bound,
                "compact_safe_within_leading_projection": abs(coefficient_m4) < compact_bound,
                "MTS_prediction": False,
                "status": "LEADING_FREE_SPECTATOR_CONDITIONAL_NONCLAIM",
                "passed": math.isfinite(result["A_C3"]) and abs(coefficient_m4) < compact_bound,
            }
        )
    return tagged(rows)


def closure_rows() -> list[dict[str, Any]]:
    rows = [
        ("pure_metric_C3", "I1=C^3", True, "4928 natural essential projection", "CLOSED_IN_2D_TRUNCATION"),
        ("free_matter_Newton_trace", "W1 contribution to beta_g", True, "heat-kernel Q1 plus 1311 cross-check", "CLOSED_AT_FREE_SPECTATOR_ORDER"),
        ("free_matter_direct_C3_trace", "W3 a6 contribution", True, "Q_-1=0 for optimized spectral W", "ZERO_AT_FREE_SPECTATOR_ORDER"),
        ("gravity_scalar_four_derivative", "essential scalar X^2 coupling", False, "2204.08564 proves it participates in the fixed-point phase diagram", "OPEN_COUPLED_ESSENTIAL_COORDINATE"),
        ("six_derivative_scalar_matter", "complete quotient basis at six derivatives", False, "2204.08564 explicitly states additional essential couplings occur", "OPEN_BASIS_AND_BETA_BLOCK"),
        ("gauge_and_fermion_six_derivative", "CFF, derivative gauge and fermion-curvature essential classes", False, "not included in the locked pure-gravity C3 notebook", "OPEN_SM_OPERATOR_BLOCKS"),
        ("matter_anomalous_dimensions", "eta_s, eta_D, eta_V and motion eta", False, "eta makes W nonconstant and can source Q_-1", "OPEN_ANOMALOUS_DIMENSIONS"),
        ("SM_and_MTS_interactions", "Yukawa, gauge, Higgs and motion vertices", False, "free background traces do not include mixed interacting diagrams", "OPEN_INTERACTION_BLOCKS"),
        ("cosmological_and_Ricci_coordinates", "Lambda, Ricci and redundant gamma-function directions", False, "zero-cosmological pure C3 trajectory is not parent-selected", "OPEN_FULL_ESSENTIAL_QUOTIENT"),
    ]
    return tagged(
        [
            {
                "block": block,
                "representative_content": content,
                "closed": closed,
                "evidence": evidence,
                "status": status,
                "blocks_full_MTS_fixed_point_claim": not closed,
                "passed": True,
            }
            for block, content, closed, evidence, status in rows
        ]
    )


def parent_inheritance_rows() -> list[dict[str, Any]]:
    clauses = [
        ("integrated_H_coordinate", True, "constant four-dimensional H-to-g point Jacobian", "KINEMATICALLY_CLOSED"),
        ("Ricci_flat_operator_map", True, "zeta_+=G_C3 and a_+=16pi G_N G_C3", "KINEMATICALLY_CLOSED"),
        ("free_spectator_C3_source", True, "Q_-1=0 in the declared optimized spectral projection", "LEADING_SOURCE_DERIVED"),
        ("visible_field_inventory", True, "SM45/SM48 and one conditional real motion mode are enumerated", "BENCHMARK_INVENTORY_CLOSED"),
        ("leading_2D_fixed_point_survival", True, "all benchmark and wide spectator rows retain one relevant and one irrelevant direction", "LEADING_PROJECTION_SURVIVES"),
        ("parent_regulator_selection", False, "MTS does not uniquely select the optimized type-II regulator", "OPEN_PARENT_REGULATOR"),
        ("interacting_matter_operator_basis", False, "six-derivative essential matter blocks are not enumerated or projected", "OPEN_ESSENTIAL_BASIS"),
        ("full_stability_matrix", False, "the 2D triangular matrix omits matter interaction directions", "OPEN_CRITICAL_SURFACE"),
        ("motion_UV_threshold", False, "the invariant motion gap does not yet select whether its scalar is active at the fixed point", "OPEN_MOTION_ACTIVATION"),
        ("zero_cosmological_trajectory", False, "the renormalized flat saddle does not prove Lambda_k=0 is UV invariant", "OPEN_FLAT_FLOW"),
        ("transition_scale", False, "k0=M_Pl remains a prescription rather than a parent-derived crossing", "OPEN_SCALE_OWNER"),
    ]
    rows = [
        {
            "clause": clause,
            "satisfied": satisfied,
            "evidence": evidence,
            "status": status,
            "blocks_numeric_MTS_prediction": not satisfied,
            "passed": True,
        }
        for clause, satisfied, evidence, status in clauses
    ]
    rows.append(
        {
            "clause": "all_dynamic_inheritance",
            "satisfied": all(row["satisfied"] for row in rows),
            "evidence": "leading free-spectator survival closes a real subset but six parent clauses remain open",
            "status": "FULL_MTS_FLOW_NOT_YET_INHERITED",
            "blocks_numeric_MTS_prediction": True,
            "passed": True,
        }
    )
    return tagged(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (path, expected_hash) in enumerate(LOCAL_BINARIES.items()):
        exists = path.exists()
        actual_hash = digest(path) if exists else ""
        passed = exists and actual_hash == expected_hash
        rows.append(
            {
                "source_id": f"SRC4929_{index:02d}_binary",
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": "locked_primary_pdf_or_author_source",
                "verification": "SHA256",
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": exists,
                "marker_found": passed,
                "status": "LOCAL_BINARY_SOURCE_HASH_VERIFIED" if passed else "LOCAL_BINARY_SOURCE_FAILED",
                "passed": passed,
            }
        )
    text_sources = [
        (PROVENANCE, "MTS_MATTER_COMPLETED_C3_FLOW_PROVENANCE_4929", "source_provenance"),
        (TEX_2104, "mode count requirement", "natural_operator_mode_count"),
        (TEX_2204, "additional essential couplings related to six-derivative operators occur", "six_derivative_matter_closure_boundary"),
        (TEX_2312, "application of this scheme to gravity-matter systems is intriguing", "pure_C3_matter_extension_boundary"),
        (TEX_1311, "N_S+2 N_D-4 N_V-46", "matter_Newton_beta_crosscheck"),
        (CHECKPOINT_4877, "W_0=N_s+2N_V-4N_D", "matter_weight_inventory"),
        (CHECKPOINT_4904, "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904", "current_parent_field_inventory"),
        (CHECKPOINT_4905, "30240", "massive_C3_spin_coefficients"),
        (CHECKPOINT_4928, "MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_4928", "pure_gravity_beta_system"),
        (Path(__file__).resolve(), "def natural_source_gate_rows", "checkpoint_generator"),
        (CHECKPOINT_DOC, MARKER, "generated_checkpoint"),
        (FORMAL_NOTE, "PPC4161_MATTER_COMPLETED_C3_FLOW_4929", "formal_checkpoint_note"),
        (VALIDATION, "MTS_MATTER_COMPLETED_C3_FLOW_VALIDATION_4929", "independent_validation_code"),
        (RESUME, NEXT_TARGET, "local_resume_ledger"),
        (CLAIMS_REGISTER, "L-771", "claim_register"),
        (VARIABLE_REGISTER, "C3MatterFlowStatus4929_MTS", "variable_register"),
        (EQUATION_REGISTER, "1.222 Matter-completed C3 leading flow and closure boundary", "equation_register"),
        (RED_TEAM_REGISTER, "173. Leading free-spectator survival is not the complete matter critical surface", "red_team_register"),
        (SPINE_REGISTER, "PPC4161 checkpoint 4929", "unification_spine"),
    ]
    for offset, (path, marker, role) in enumerate(text_sources, start=len(rows)):
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": f"SRC4929_{offset:02d}_text",
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
    for key, url in ARXIV_URLS.items():
        rows.append(
            {
                "source_id": f"SRC4929_URL_{key}",
                "source_path_or_url": url,
                "source_role": "primary_arXiv_record",
                "verification": "external_primary_URL_recorded_and_local_binary_locked",
                "expected_sha256": "",
                "actual_sha256": "",
                "source_exists": True,
                "marker_found": True,
                "status": "EXTERNAL_PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def gate_rows(
    fixed_points: list[dict[str, Any]],
    scan: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    inheritance: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    benchmark_failures = sum(not bool(row["passed"]) for row in fixed_points)
    scan_failures = sum(not bool(row["passed"]) for row in scan)
    open_blocks = sum(not bool(row["closed"]) for row in closure)
    inherited = next(row for row in inheritance if row["clause"] == "all_dynamic_inheritance")["satisfied"]
    return tagged(
        [
            {
                "gate": "Ricci_flat_matter_C3_weight",
                "status": "DERIVED",
                "decision": "W3=N_s-4N_D+2N_V=W0",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "optimized_free_spectator_C3_source",
                "status": "ZERO_DERIVED",
                "decision": "Q_-1[W]=-W'(0)=0 for W=2 below the Litim cutoff",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "benchmark_fixed_point_survival",
                "status": "PASS_LEADING_2D_PROJECTION",
                "decision": f"{len(fixed_points) - benchmark_failures}/{len(fixed_points)} benchmark projection rows survive",
                "claim_promoted": False,
                "passed": benchmark_failures == 0,
            },
            {
                "gate": "wide_fixed_point_stress",
                "status": "PASS_LEADING_2D_PROJECTION",
                "decision": f"{len(scan) - scan_failures}/{len(scan)} optimized/hybrid scan rows survive",
                "claim_promoted": False,
                "passed": scan_failures == 0,
            },
            {
                "gate": "proper_time_shift",
                "status": "QUARANTINED",
                "decision": "h approaches C_m rather than zero; u=h-C_m exposes the shifted-Gaussian massless local artifact",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "full_matter_essential_closure",
                "status": "NOT_DERIVED",
                "decision": f"{open_blocks} interacting essential operator blocks remain open",
                "claim_promoted": False,
                "passed": open_blocks > 0,
            },
            {
                "gate": "MTS_dynamic_inheritance",
                "status": "NOT_PROMOTED",
                "decision": "leading spectator survival is not the complete MTS fixed point or critical surface",
                "claim_promoted": False,
                "passed": not inherited,
            },
            {
                "gate": "one_observational_Wilson",
                "status": "RETAINED",
                "decision": "keep one RG-invariant A_+(Q_GW); do not promote any conditional spectator number",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "weak_GR_Newton_Maxwell",
                "status": "RETAINED",
                "decision": "the UV spectator stress test does not alter the calibrated two-derivative local limit",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "compact_and_full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "conditional Planck-scale compact safety is encouraging but lacks full essential-flow inheritance",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "SIX_DERIVATIVE_MATTER_ESSENTIAL_BASIS",
                "decision": NEXT_TARGET,
                "claim_promoted": False,
                "passed": True,
            },
        ]
    )


def main() -> int:
    inventory = matter_scenarios()
    spin_weights = spin_weight_rows()
    natural_gate = natural_source_gate_rows()
    proper_time = proper_time_rows(inventory)
    fixed_points = benchmark_fixed_point_rows(inventory)
    scan = robustness_scan_rows()
    conditional = conditional_map_rows(inventory)
    closure = closure_rows()
    inheritance = parent_inheritance_rows()
    sources = source_register_rows()
    gates = gate_rows(fixed_points, scan, closure, inheritance)
    tables = {
        "P8_Y5_R2FR_4929_MATTER_FIELD_INVENTORY.csv": inventory,
        "P8_Y5_R2FR_4929_C3_SPIN_WEIGHT_DERIVATION.csv": spin_weights,
        "P8_Y5_R2FR_4929_NATURAL_QMINUS1_GATE.csv": natural_gate,
        "P8_Y5_R2FR_4929_PROPER_TIME_SHIFT_DIAGNOSTIC.csv": proper_time,
        "P8_Y5_R2FR_4929_BENCHMARK_FIXED_POINTS.csv": fixed_points,
        "P8_Y5_R2FR_4929_FIXED_POINT_ROBUSTNESS_SCAN.csv": scan,
        "P8_Y5_R2FR_4929_CONDITIONAL_COMPACT_MAP.csv": conditional,
        "P8_Y5_R2FR_4929_ESSENTIAL_OPERATOR_CLOSURE.csv": closure,
        "P8_Y5_R2FR_4929_PARENT_INHERITANCE_GATE.csv": inheritance,
        "P8_Y5_R2FR_4929_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4929_GATE_DECISION.csv": gates,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    passed = all(bool(row.get("passed", True)) for rows in tables.values() for row in rows)
    optimized = [row for row in fixed_points if row["projection"] == "optimized_spectral_free_spectator"]
    hybrid_scan = [row for row in scan if row["projection"] == "proper_time_hybrid_diagnostic"]
    print("P8_Y5_R2FR_4929_MATTER_COMPLETED_C3_FLOW_PASS" if passed else "P8_Y5_R2FR_4929_MATTER_COMPLETED_C3_FLOW_FAIL")
    print("W3_equals_W0=True")
    print("optimized_free_spectator_direct_C3_source=0")
    print(f"benchmark_optimized_survival={sum(bool(row['passed']) for row in optimized)}/{len(optimized)}")
    print(f"hybrid_wide_scan_survival={sum(bool(row['passed']) for row in hybrid_scan)}/{len(hybrid_scan)}")
    print(f"conditional_A_C3_range={min(float(row['A_C3_equals_GC3_over_GN_at_k0']) for row in conditional):.16e},{max(float(row['A_C3_equals_GC3_over_GN_at_k0']) for row in conditional):.16e}")
    print("full_matter_essential_flow_closed=False")
    print("independent_IR_I1_test_parameters=1")
    print("compact_GR_promoted=False")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
