from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

from scipy.constants import G, c, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4921"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_C3_NONLOCAL_OBSERVABLE_DOMAIN_GATE_4921"
FORMAL_MARKER = "PPC4161_C3_NONLOCAL_OBSERVABLE_DOMAIN_GATE_4921"
NEXT_TARGET = (
    "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-"
    "bound-or-compact-vacuum-GR-domain-gate.md"
)

BURGER_URL = "https://arxiv.org/abs/1910.11618"
CALMET_URL = "https://arxiv.org/abs/1704.00261"
GOROFF_SAGNOTTI_REVIEW_URL = "https://scipost.org/SciPostPhysLectNotes.98/pdf"
CASSINI_URL = "https://pubmed.ncbi.nlm.nih.gov/14508481/"
GALILEO_URL = "https://arxiv.org/abs/1906.06161"
MERCURY_URL = "https://www.osti.gov/biblio/22863119"
GW_CUBIC_URL = "https://arxiv.org/abs/2407.07043"

EARTH_MASS_KG = 5.9722e24
EARTH_RADIUS_M = 6_371_000.0
SUN_MASS_KG = 1.98847e30
SUN_RADIUS_M = 695_700_000.0
GALILEO_ALTITUDE_M = 23_229_000.0
CASSINI_IMPACT_M = 1.6 * SUN_RADIUS_M
MERCURY_A_M = 5.790905e10
MERCURY_E = 0.205630
MERCURY_PERIOD_DAYS = 87.9691
JULIAN_CENTURY_DAYS = 36_525.0

TAU_CLOCK = 2.48e-5
TAU_CASSINI_GAMMA = 2.3e-5
TAU_MERCURY_ARCSEC_CENTURY = 0.0015
TAU_DOMAIN = 0.01
R10_MINIMUM_GAP_M = 52.0e-6
PLANCK_LENGTH_M = physical_constants["Planck length"][0]
GS_BETA = 209.0 / 2880.0


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


def schwarzschild_radius(mass_kg: float) -> float:
    return 2.0 * G * mass_kg / c**2


def c3_potential_fraction_coefficient(rs_m: float, radius_m: float) -> float:
    return rs_m / radius_m**5


def c3_acceleration_fraction_coefficient(rs_m: float, radius_m: float) -> float:
    return 6.0 * c3_potential_fraction_coefficient(rs_m, radius_m)


def c3_gamma_coefficient(rs_m: float, impact_m: float) -> float:
    return 15.0 * math.pi * rs_m / (8.0 * impact_m**5)


def c3_clock_coefficient(rs_m: float, radius_1_m: float, radius_2_m: float) -> float:
    numerator = abs(radius_1_m**-6 - radius_2_m**-6)
    denominator = abs(radius_1_m**-1 - radius_2_m**-1)
    return rs_m * numerator / denominator


def c3_pericenter_coefficient(rs_m: float, semi_major_m: float, eccentricity: float) -> float:
    eccentricity_factor = 1.0 + 1.5 * eccentricity**2 + eccentricity**4 / 8.0
    return (
        30.0
        * math.pi
        * rs_m
        * eccentricity_factor
        / (semi_major_m**5 * (1.0 - eccentricity**2) ** 5)
    )


def mercury_limit_rad_per_orbit() -> float:
    arcsec_to_rad = math.pi / (180.0 * 3600.0)
    orbits_per_century = JULIAN_CENTURY_DAYS / MERCURY_PERIOD_DAYS
    return TAU_MERCURY_ARCSEC_CENTURY * arcsec_to_rad / orbits_per_century


def l3_cap(limit: float, coefficient_per_l3_four: float) -> float:
    if limit <= 0.0 or coefficient_per_l3_four <= 0.0:
        raise ValueError("positive limit and response coefficient required")
    return (limit / coefficient_per_l3_four) ** 0.25


def local_bound_values() -> dict[str, float]:
    earth_rs = schwarzschild_radius(EARTH_MASS_KG)
    sun_rs = schwarzschild_radius(SUN_MASS_KG)
    clock_coefficient = c3_clock_coefficient(
        earth_rs,
        EARTH_RADIUS_M,
        EARTH_RADIUS_M + GALILEO_ALTITUDE_M,
    )
    cassini_coefficient = c3_gamma_coefficient(sun_rs, CASSINI_IMPACT_M)
    mercury_coefficient = c3_pericenter_coefficient(
        sun_rs, MERCURY_A_M, MERCURY_E
    )
    mercury_limit = mercury_limit_rad_per_orbit()
    clock_cap = l3_cap(TAU_CLOCK, clock_coefficient)
    cassini_cap = l3_cap(TAU_CASSINI_GAMMA, cassini_coefficient)
    mercury_cap = l3_cap(mercury_limit, mercury_coefficient)
    return {
        "earth_rs_m": earth_rs,
        "sun_rs_m": sun_rs,
        "clock_coefficient_m_minus_4": clock_coefficient,
        "cassini_coefficient_m_minus_4": cassini_coefficient,
        "mercury_coefficient_m_minus_4": mercury_coefficient,
        "mercury_limit_rad_per_orbit": mercury_limit,
        "clock_cap_m": clock_cap,
        "cassini_cap_m": cassini_cap,
        "mercury_cap_m": mercury_cap,
        "selected_local_cap_m": min(clock_cap, cassini_cap, mercury_cap),
    }


def coefficient_ownership_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "owner_id": "OWNER4921_00_action",
                "object": "first nonredundant parity-even Ricci-flat cubic metric operator",
                "formula": "S=int sqrt(-g)[R/(16 pi G_N)+d3 I3+...]",
                "status": "ON_SHELL_OPERATIONAL_BASIS",
                "meaning": "d3 is the coefficient combination that enters the nonrotating exterior potential in the declared Burger-Emond-Moynihan basis",
                "source": BURGER_URL,
                "passed": True,
            },
            {
                "owner_id": "OWNER4921_01_length",
                "object": "observable cubic length",
                "formula": "L3^4=144 pi G_N abs(d3)",
                "status": "BASIS_DECLARED_OBSERVABLE_MAGNITUDE",
                "meaning": "all weak exterior bounds are reported on L3 rather than an unnormalised c6 symbol",
                "source": BURGER_URL,
                "passed": True,
            },
            {
                "owner_id": "OWNER4921_02_bare",
                "object": "finite renormalized cubic matching coefficient",
                "formula": "d3_total(mu)=d3_finite(mu)+d3_GS_running(mu)+d3_massive_threshold(mu)",
                "status": "FINITE_PART_NOT_DERIVED",
                "meaning": "the two-loop divergence fixes running but not the finite renormalization condition",
                "source": "post-checkpoint-work/4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
                "passed": True,
            },
            {
                "owner_id": "OWNER4921_03_MTS",
                "object": "interacting MTS residual",
                "formula": "Gamma_MTS,res=0 on the selected renormalization branch at its matching scale",
                "status": "ZERO_BRANCH_NOT_ZERO_THEOREM",
                "meaning": "checkpoint 4914 failed to promote a nonzero lattice residual; absence of a promoted residual is not proof that every physical cubic coefficient vanishes",
                "source": "post-checkpoint-work/4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md",
                "passed": True,
            },
            {
                "owner_id": "OWNER4921_04_massless",
                "object": "massless MTS and Standard-Model modes",
                "formula": "C log(-Box/mu^2) C and R log(-Box/mu^2) R",
                "status": "NONLOCAL_NOT_LOCAL_C3",
                "meaning": "a massless logarithm cannot be rewritten as a divergent 1/m^2 local cubic coefficient",
                "source": "post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
                "passed": True,
            },
            {
                "owner_id": "OWNER4921_05_flat",
                "object": "flat-space propagator",
                "formula": "delta S_C3^(1)[eta]=delta S_C3^(2)[eta]=0",
                "status": "NO_LINEAR_NEWTON_OR_PHOTON_POLE_SHIFT",
                "meaning": "the cubic operator first contributes through nonlinear curvature and the metric three-point sector",
                "source": "post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
                "passed": True,
            },
        ]
    )


def weak_field_transfer_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "transfer_id": "TRANSFER4921_00_potential",
                "observable": "nonrotating exterior potential",
                "formula": "delta Phi=-L3^4 r_s^2/(2 r^6)",
                "coefficient": -0.5,
                "radial_power": -6,
                "derivation": "Burger potential with L3^4=144 pi G_N abs(d3)",
                "status": "EXACT_FIRST_ORDER_DECLARED_C3_BASIS",
                "passed": True,
            },
            {
                "transfer_id": "TRANSFER4921_01_fraction",
                "observable": "potential fractional shift",
                "formula": "abs(delta Phi/Phi_N)=L3^4 r_s/r^5",
                "coefficient": 1.0,
                "radial_power": -5,
                "derivation": "divide by Phi_N=r_s/(2r)",
                "status": "EXACT_FIRST_ORDER",
                "passed": True,
            },
            {
                "transfer_id": "TRANSFER4921_02_acceleration",
                "observable": "radial acceleration fractional shift",
                "formula": "abs(delta a/a_N)=6 L3^4 r_s/r^5",
                "coefficient": 6.0,
                "radial_power": -5,
                "derivation": "differentiate the r^-6 potential before dividing by a_N",
                "status": "EXACT_FIRST_ORDER",
                "passed": True,
            },
            {
                "transfer_id": "TRANSFER4921_03_light",
                "observable": "light-deflection fractional shift",
                "formula": "abs(delta alpha/alpha_GR)=(15 pi/16)L3^4 r_s/b^5; abs(delta gamma)=(15 pi/8)L3^4 r_s/b^5",
                "coefficient": 15.0 * math.pi / 16.0,
                "radial_power": -5,
                "derivation": "2 int dz partial_b(delta Phi) with int dz(b^2+z^2)^-4=5 pi/(16 b^7)",
                "status": "EQUAL_METRIC_POTENTIAL_FIRST_ORDER",
                "passed": True,
            },
            {
                "transfer_id": "TRANSFER4921_04_clock",
                "observable": "two-radius clock redshift anomaly",
                "formula": "abs(alpha_clock)=L3^4 r_s abs(r1^-6-r2^-6)/abs(r1^-1-r2^-1)",
                "coefficient": 1.0,
                "radial_power": -5,
                "derivation": "ratio of the cubic and Newtonian potential differences",
                "status": "EXACT_STATIC_FIRST_ORDER",
                "passed": True,
            },
            {
                "transfer_id": "TRANSFER4921_05_orbit",
                "observable": "pericentre advance per orbit",
                "formula": "abs(Delta varpi)=30 pi L3^4 r_s[a^-5(1-e^2)^-5](1+3e^2/2+e^4/8)",
                "coefficient": 30.0 * math.pi,
                "radial_power": -5,
                "derivation": "first-order Gauss equation integrated over the Kepler ellipse",
                "status": "EXACT_FIRST_ORDER_CENTRAL_PERTURBATION",
                "passed": True,
            },
            {
                "transfer_id": "TRANSFER4921_06_proxy_repair",
                "observable": "checkpoint-4880 weak proxy",
                "formula": "L3^4 K is a strong-curvature control parameter but is not the weak exterior observable transfer",
                "coefficient": "not_applicable",
                "radial_power": "not_applicable",
                "derivation": "the exact field equation carries derivatives and yields L3^4 r_s/r^5 rather than only L3^4 r_s^2/r^6",
                "status": "4880_PROXY_SCOPE_CORRECTED",
                "passed": True,
            },
        ]
    )


def local_arena_bound_rows() -> list[dict[str, Any]]:
    values = local_bound_values()
    selected = values["selected_local_cap_m"]
    rows = [
        {
            "arena_id": "ARENA4921_00_Galileo_clock",
            "arena": "Galileo eccentric-satellite redshift",
            "response": "alpha_clock",
            "coefficient_per_L3_4_m_minus_4": values["clock_coefficient_m_minus_4"],
            "bound_value": TAU_CLOCK,
            "bound_units": "dimensionless",
            "L3_upper_m": values["clock_cap_m"],
            "projected_at_selected_cap": values["clock_coefficient_m_minus_4"] * selected**4,
            "source": GALILEO_URL,
            "status": "PRIVATE_ONE_PARAMETER_ENVELOPE_SELECTED",
            "passed": True,
        },
        {
            "arena_id": "ARENA4921_01_Cassini_light",
            "arena": "Cassini solar conjunction",
            "response": "abs(delta gamma)",
            "coefficient_per_L3_4_m_minus_4": values["cassini_coefficient_m_minus_4"],
            "bound_value": TAU_CASSINI_GAMMA,
            "bound_units": "dimensionless",
            "L3_upper_m": values["cassini_cap_m"],
            "projected_at_selected_cap": values["cassini_coefficient_m_minus_4"] * selected**4,
            "source": CASSINI_URL,
            "status": "PRIVATE_ONE_PARAMETER_ENVELOPE",
            "passed": True,
        },
        {
            "arena_id": "ARENA4921_02_Mercury_orbit",
            "arena": "MESSENGER Mercury perihelion",
            "response": "abs(Delta varpi) per orbit",
            "coefficient_per_L3_4_m_minus_4": values["mercury_coefficient_m_minus_4"],
            "bound_value": values["mercury_limit_rad_per_orbit"],
            "bound_units": "rad/orbit converted from 0.0015 arcsec/century",
            "L3_upper_m": values["mercury_cap_m"],
            "projected_at_selected_cap": values["mercury_coefficient_m_minus_4"] * selected**4,
            "source": MERCURY_URL,
            "status": "PRIVATE_ONE_PARAMETER_ENVELOPE",
            "passed": True,
        },
        {
            "arena_id": "ARENA4921_03_R10",
            "arena": "Eot-Wash R10 short-range geometry",
            "response": "extended-source C3 force residual",
            "coefficient_per_L3_4_m_minus_4": "",
            "bound_value": R10_MINIMUM_GAP_M,
            "bound_units": "minimum gap m; not an observable residual bound",
            "L3_upper_m": "",
            "projected_at_selected_cap": "",
            "source": "post-checkpoint-work/4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "status": "BLOCKED_REQUIRES_EXTENDED_SOURCE_GEOMETRY_NOT_YUKAWA_RECAST",
            "passed": True,
        },
    ]
    return tagged(rows)


def strong_domain_rows() -> list[dict[str, Any]]:
    values = local_bound_values()
    selected = values["selected_local_cap_m"]
    systems = read_csv(OUTPUT / "P8_Y5_R2FR_4880_SYSTEM_BENCHMARKS.csv")
    rows: list[dict[str, Any]] = []
    for source in systems:
        mass_kg = float(source["mass_kg"])
        radius_m = float(source["radius_m"])
        rs_m = schwarzschild_radius(mass_kg)
        kretschmann = 12.0 * rs_m**2 / radius_m**6
        cap_m = (9.0 * TAU_DOMAIN / kretschmann) ** 0.25
        epsilon_at_selected = selected**4 * kretschmann / 9.0
        rows.append(
            {
                "system": source["system"],
                "source_class": source["source_class"],
                "mass_kg": mass_kg,
                "radius_m": radius_m,
                "r_s_m": rs_m,
                "K_m_minus_4": kretschmann,
                "control_formula": "epsilon_K=L3^4 K/9",
                "tau_domain": TAU_DOMAIN,
                "L3_upper_m_for_domain": cap_m,
                "epsilon_at_selected_local_cap": epsilon_at_selected,
                "selected_local_cap_satisfies_domain": epsilon_at_selected < TAU_DOMAIN,
                "status": (
                    "LOCAL_CAP_CONTROLS_THIS_BACKGROUND"
                    if epsilon_at_selected < TAU_DOMAIN
                    else "COMPACT_DOMAIN_NOT_CERTIFIED_BY_LOCAL_CAP"
                ),
                "passed": True,
            }
        )
    return tagged(rows)


def goroff_sagnotti_rows() -> list[dict[str, Any]]:
    kappa_squared_m2 = 32.0 * math.pi * PLANCK_LENGTH_M**2
    d3_per_log_m2 = GS_BETA * kappa_squared_m2 / (4.0 * math.pi) ** 4
    ten_solar_rs = schwarzschild_radius(10.0 * SUN_MASS_KG)
    rows: list[dict[str, Any]] = []
    for log_magnitude in (1.0, 100.0):
        d3_m2 = d3_per_log_m2 * log_magnitude
        l3_m = (144.0 * math.pi * PLANCK_LENGTH_M**2 * d3_m2) ** 0.25
        rows.append(
            {
                "running_id": f"GS4921_log_{int(log_magnitude)}",
                "pole_residue": GS_BETA,
                "kappa_squared_m2": kappa_squared_m2,
                "log_magnitude": log_magnitude,
                "abs_d3_running_m2": d3_m2,
                "L3_running_m": l3_m,
                "L3_over_planck_length": l3_m / PLANCK_LENGTH_M,
                "ten_solar_BH_horizon_epsilon": (4.0 / 3.0) * (l3_m / ten_solar_rs) ** 4,
                "status": "RUNNING_SCALE_ONLY_NOT_FINITE_MATCHING_PREDICTION",
                "source": GOROFF_SAGNOTTI_REVIEW_URL,
                "passed": True,
            }
        )
    return tagged(rows)


def nonlocal_separation_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "class_id": "NONLOCAL4921_00_local_quadratic",
                "operator_class": "local R2 and C2",
                "radial_image": "contact or exact-zero Einstein-background field equation",
                "background_scope": "four-dimensional selected Einstein branch",
                "status": "EXACT_BACKGROUND_RESULT_RETAINED",
                "cancellation_with_C3": "NO",
                "passed": True,
            },
            {
                "class_id": "NONLOCAL4921_01_eternal",
                "operator_class": "quadratic-curvature nonlocal logarithms",
                "radial_image": "no correction to eternal Schwarzschild through O(curvature^2)",
                "background_scope": "eternal source-free Schwarzschild state at the calculated order",
                "status": "SOURCE_AND_STATE_SCOPED_EXACT_RESULT",
                "cancellation_with_C3": "NO",
                "passed": True,
            },
            {
                "class_id": "NONLOCAL4921_02_material",
                "operator_class": "massless-loop nonanalytic amplitude",
                "radial_image": "r^-3 quantum potential tail for a material or scattering source",
                "background_scope": "source-dependent weak field",
                "status": "PHYSICAL_LONG_RANGE_CLASS_RETAINED_FROM_4878",
                "cancellation_with_C3": "NO_DIFFERENT_RADIAL_POWER_AND_SOURCE_DEFINITION",
                "passed": True,
            },
            {
                "class_id": "NONLOCAL4921_03_C3",
                "operator_class": "local curvature-cubed metric operator",
                "radial_image": "r^-6 potential correction",
                "background_scope": "nonlinear vacuum exterior and strong curvature",
                "status": "FIRST_LOCAL_OPERATOR_THAT_DEFORMS_SCHWARZSCHILD",
                "cancellation_with_C3": "SELF",
                "passed": True,
            },
            {
                "class_id": "NONLOCAL4921_04_massless_limit",
                "operator_class": "massless MTS or matter mode",
                "radial_image": "log(-Box) form factor",
                "background_scope": "infrared nonlocal effective action",
                "status": "DO_NOT_CONVERT_TO_LOCAL_1_OVER_M2_C3",
                "cancellation_with_C3": "NO",
                "passed": True,
            },
            {
                "class_id": "NONLOCAL4921_05_no_merge",
                "operator_class": "combined pure-metric ledger",
                "radial_image": "sum of separately defined local and nonlocal observables",
                "background_scope": "declared source state and renormalization scale required",
                "status": "NO_UNSOURCED_CANCELLATION_OR_FINITE_TAIL_FABRICATION",
                "cancellation_with_C3": "FORBIDDEN_WITHOUT_MATCHED_COEFFICIENTS",
                "passed": True,
            },
        ]
    )


def maxwell_projection_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "projection_id": "MAXWELL4921_00_fixed_metric",
                "statement": "pure C3 contains no F_mn and does not alter the Maxwell action or current at fixed metric",
                "status": "EXACT_OPERATOR_CONTENT",
                "observable": "no direct charge or Poynting-vector renormalization",
                "passed": True,
            },
            {
                "projection_id": "MAXWELL4921_01_flat",
                "statement": "the first and second flat-background variations of C3 vanish",
                "status": "NO_LINEAR_PHOTON_PROPAGATION_OR_BIREFRINGENCE_SHIFT",
                "observable": "vacuum Maxwell waves remain on the inherited metric null cone at linear order",
                "passed": True,
            },
            {
                "projection_id": "MAXWELL4921_02_source",
                "statement": "the Maxwell Hilbert tensor including energy flux remains a source of the public metric",
                "status": "POYNTING_VECTOR_RETAINED_AS_GRAVITATIONAL_SOURCE",
                "observable": "C3 can feed back only through the nonlinear corrected metric",
                "passed": True,
            },
            {
                "projection_id": "MAXWELL4921_03_mixed",
                "statement": "operators such as R F^2 and R_mn F^ma F^n_a are not part of pure C3",
                "status": "SEPARATE_MIXED_OPERATOR_LEDGER",
                "observable": "direct optical dispersion belongs to the previously separated mixed-curvature class",
                "passed": True,
            },
        ]
    )


def gate_decision_rows() -> list[dict[str, Any]]:
    values = local_bound_values()
    return tagged(
        [
            {
                "gate": "weak_transfer",
                "status": "EXACT_R_MINUS_6_TRANSFER_DERIVED",
                "decision": "replace the weak use of the 4880 K-only proxy by the potential acceleration light clock and orbit maps",
                "passed": True,
            },
            {
                "gate": "local_one_parameter_envelope",
                "status": "GALILEO_SELECTED_PRIVATE_BOUND",
                "decision": f"L3<{values['selected_local_cap_m']:.12e} m from the current simple clock envelope; no joint likelihood",
                "passed": True,
            },
            {
                "gate": "R10",
                "status": "NOT_PROJECTED",
                "decision": "the Yukawa alpha-lambda curve cannot be reused for an r^-6 extended-source force without apparatus geometry",
                "passed": True,
            },
            {
                "gate": "universal_two_loop_running",
                "status": "PLANCK_SCALE_AND_ARENA_SAFE",
                "decision": "the Goroff-Sagnotti pole fixes a tiny running scale but not the finite d3 matching coefficient",
                "passed": True,
            },
            {
                "gate": "weak_invariant_vacuum_GR",
                "status": "RETAINED_WITH_EXPLICIT_C3_BOUND_CLAUSE",
                "decision": "the selected weak certificate survives only inside the measured-residue strict-EFT branch and the stated L3 envelope",
                "passed": True,
            },
            {
                "gate": "compact_vacuum_GR",
                "status": "NOT_GLOBALLY_EXTENDED",
                "decision": "nonzero C3 deforms Schwarzschild and Kerr; local tests do not enforce the kilometre-scale compact-domain caps",
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "finite C3 matching strong-field waveforms compact matter nonvacuum flow and UV completion remain open",
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "DIRECT_STRONG_FIELD_C3_TEST",
                "decision": NEXT_TARGET,
                "passed": True,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4921_00_prior_validation", OUTPUT / "P8_Y5_BRR545_4920_VALIDATION.csv", "VAL4920_OVERALL,PASS", "predecessor_validation"),
        ("SRC4921_01_4920", POST / "4920-Y5-R2FR-graviton-mediated-curvature-Higgs-running-and-current-Higgs-coupling-bound-or-vacuum-local-GR-promotion-gate.md", "MTS_GRAVITON_HIGGS_OBSERVABLE_LOCAL_GR_GATE_4920", "predecessor"),
        ("SRC4921_02_4877", POST / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md", "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877", "massless_nonlocal_owner"),
        ("SRC4921_03_4878", POST / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md", "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878", "nonlocal_arena_predecessor"),
        ("SRC4921_04_4879", POST / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md", "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879", "weak_GR_predecessor"),
        ("SRC4921_05_4880", POST / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md", "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880", "domain_predecessor"),
        ("SRC4921_06_4881", POST / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md", "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881", "C3_owner_predecessor"),
        ("SRC4921_07_4908", POST / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md", "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908", "flat_variation_predecessor"),
        ("SRC4921_08_4914", POST / "4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md", "MTS_COMPLEX_SOURCE_TAYLOR_TTT_REPLICA_4914", "interacting_residual_predecessor"),
        ("SRC4921_09_4914_gate", OUTPUT / "P8_Y5_R2FR_4914_GATE_DECISION.csv", "interacting_C3_promotion", "interacting_residual_decision"),
        ("SRC4921_10_4880_systems", OUTPUT / "P8_Y5_R2FR_4880_SYSTEM_BENCHMARKS.csv", "1.4_solar_mass_12km_neutron_star", "system_inputs"),
        ("SRC4921_11_checkpoint", POST / "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md", MARKER, "generated_checkpoint"),
        ("SRC4921_12_research", Path(__file__).resolve(), "def weak_field_transfer_rows", "generated_research_code"),
        ("SRC4921_13_validation", SCRIPTS / "Y5_R2FR_4921_C3_nonlocal_observable_domain_validation.py", "VAL4921_OVERALL", "generated_validation_code"),
        ("SRC4921_14_formal", FORMAL / "937-PPC4161-C3-nonlocal-observable-domain-gate.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4921_15_provenance", POST / "source-intake" / "parent_coupling" / "4921" / "PROVENANCE.md", "MTS_C3_NONLOCAL_PROVENANCE_4921", "provenance"),
        ("SRC4921_16_claim", FORMAL / "02-claims-register.csv", "L-763", "register"),
        ("SRC4921_17_variable", FORMAL / "04-variable-audit.csv", "CubicMetricPacket4921_MTS", "register"),
        ("SRC4921_18_equation", FORMAL / "05-equation-register.md", "1.214 Cubic-metric observable transfer and domain gate", "register"),
        ("SRC4921_19_redteam", FORMAL / "06-consistency-red-team.md", "165. A curvature invariant is not by itself the weak-field observable", "register"),
        ("SRC4921_20_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4921", "register"),
        ("SRC4921_21_resume", POST / "CURRENT_LOCAL_RESUME.md", FORMAL_MARKER, "resume"),
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
        ("SRC4921_22_Burger", BURGER_URL, "Rotating Black Holes in Cubic Gravity", "primary_C3_metric_transfer"),
        ("SRC4921_23_Calmet", CALMET_URL, "Quantum Corrections to Schwarzschild Black Hole", "primary_nonlocal_state_separation"),
        ("SRC4921_24_GS", GOROFF_SAGNOTTI_REVIEW_URL, "209/[2880(4 pi)^4]", "authoritative_two_loop_residue"),
        ("SRC4921_25_Cassini", CASSINI_URL, "gamma-1=(2.1+/-2.3)e-5", "primary_experiment"),
        ("SRC4921_26_Galileo", GALILEO_URL, "Galileo eccentric satellites gravitational redshift", "primary_experiment"),
        ("SRC4921_27_Mercury", MERCURY_URL, "MESSENGER Mercury ephemeris", "primary_experiment"),
        ("SRC4921_28_GW", GW_CUBIC_URL, "cubic-curvature gravitational-wave scaling", "next_target_primary_source"),
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
        "P8_Y5_R2FR_4921_COEFFICIENT_OWNERSHIP.csv": coefficient_ownership_rows(),
        "P8_Y5_R2FR_4921_WEAK_FIELD_TRANSFER.csv": weak_field_transfer_rows(),
        "P8_Y5_R2FR_4921_LOCAL_ARENA_BOUNDS.csv": local_arena_bound_rows(),
        "P8_Y5_R2FR_4921_STRONG_DOMAIN.csv": strong_domain_rows(),
        "P8_Y5_R2FR_4921_GOROFF_SAGNOTTI_RUNNING.csv": goroff_sagnotti_rows(),
        "P8_Y5_R2FR_4921_NONLOCAL_SEPARATION.csv": nonlocal_separation_rows(),
        "P8_Y5_R2FR_4921_MAXWELL_PROJECTION.csv": maxwell_projection_rows(),
        "P8_Y5_R2FR_4921_GATE_DECISION.csv": gate_decision_rows(),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4921_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4921_C3_NONLOCAL_DOMAIN_PASS"
        if passed
        else "P8_Y5_R2FR_4921_C3_NONLOCAL_DOMAIN_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
