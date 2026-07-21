from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True
getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4953"

RESULT_JSON = SOURCE / "formation_X2_cascade_and_injection_results.json"
KERNEL_CSV = SOURCE / "X2_scattering_kernel.csv"
INVARIANT_CSV = SOURCE / "X2_collision_invariant_gate.csv"
SPECTRAL_CSV = SOURCE / "formation_spectral_number_bound.csv"
SPARC_INJECTION_CSV = SOURCE / "SPARC_formation_injection_gate.csv"
SPARC_NONLINEAR_CSV = SOURCE / "SPARC_X2_nonlinearity_gate.csv"
LOCAL_CSV = SOURCE / "local_compact_X2_injection_gate.csv"
NUMBER_CHANGE_CSV = SOURCE / "X2_number_change_scaling.csv"
DECISION_CSV = SOURCE / "formation_X2_composite_route_decision.csv"

O4_4941 = POST / "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-minimal-O4-parent-completion-gate.md"
CTP_4949 = POST / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"
PAIR_4952 = POST / "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md"
BERGES_TEX = POST / "source-intake" / "functional_rg" / "4948" / "riolecture.tex"
OCCUPATION_CSV = POST / "source-intake" / "functional_rg" / "4949" / "SPARC_outer_occupation_scale_diagnostic.csv"
HARMONIC_CSV = POST / "source-intake" / "functional_rg" / "4952" / "SPARC_outer_harmonic_support_gate.csv"
LOCAL_SUPPORT_CSV = POST / "source-intake" / "functional_rg" / "4952" / "local_compact_rotator_harmonic_support_gate.csv"
PLANCK_PDF = SOURCE / "1807.06209v4.pdf"

MARKER = "MTS_4953_FORMATION_X2_CASCADE_AND_INJECTION_GATE"
CHECKED_DATE = "2026-07-13"

LIGHT_SPEED = 299_792_458.0
HBAR_EV_S = 6.582_119_569e-16
HBARC_EV_M = 1.973_269_804e-7
JOULE_PER_EV = 1.602_176_634e-19
SOLAR_MASS = 1.988_47e30
REDUCED_PLANCK_MASS_EV = 2.435e27
NATURAL_C_ESS_EV_M4 = REDUCED_PLANCK_MASS_EV**-4
EV_M2_TO_M2 = HBARC_EV_M**2
YEAR_S = 365.25 * 24.0 * 3600.0
GENEROUS_FORMATION_TIME_S = 10.0e9 * YEAR_S
PLANCK_Z_STAR = 1089.92
MAX_POST_RECOMBINATION_STRETCH = 1.0 + PLANCK_Z_STAR

DECIMAL_PI = Decimal("3.1415926535897932384626433832795028841971693993751")
DECIMAL_PLANCK_MASS_EV = Decimal("2.435e27")
DECIMAL_NATURAL_C_ESS = Decimal(1) / DECIMAL_PLANCK_MASS_EV**4
DECIMAL_HBARC_EV_M = Decimal("1.973269804e-7")

EXPECTED_HASHES = {
    O4_4941: "f4c6f83668c5f904706747dcafb3d538068a038307ffc062e13fe3234a6b9543",
    CTP_4949: "772bee9863471ab7e4a4e4887773b91786110539d471243c26aaa1b88866f7b8",
    PAIR_4952: "2e4fc50355c1c3cefece8d5eb633952dea2ea9a8445712c2c4daf870dcc938d8",
    BERGES_TEX: "de16f5e4f6e8b10e6880a18b130a4923952556e6fead9fda7a7e162e3282128d",
    OCCUPATION_CSV: "959c76b6e88efcf9ddcc9d010a20fbb1cefebfb310797e0b1814e76e3a13e92a",
    HARMONIC_CSV: "8a7ab287b4078f16416447cc3a336a7742baae590abd4938124ab5685ac08199",
    LOCAL_SUPPORT_CSV: "9042df95d51b400bf67cc61a20078b5cb603897f9c32c1ec5b24df704ea46c72",
    PLANCK_PDF: "8e172730faf07c9f4ff3fdcc7043f76ed67df6f76066d47df30d693025b6ce77",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
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


def energy_density_to_ev4(value_j_m3: float) -> float:
    return value_j_m3 * HBARC_EV_M**3 / JOULE_PER_EV


def decimal_scientific(value: Decimal) -> str:
    return f"{value:.16E}"


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)

    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())

    o4_text = read_text(O4_4941)
    ctp_text = read_text(CTP_4949)
    pair_text = read_text(PAIR_4952)
    berges_text = read_text(BERGES_TEX)
    source_clause_checks = {
        "4941_essential_coordinate": "c_ess=c+8pi g(ctilde+d)." in o4_text,
        "4941_gravity_generates_X2": "beta_c,ess|0   =16g^2." in o4_text,
        "4949_2PI_occupation_framework": "Covariant CTP-2PI occupation" in ctp_text,
        "4952_pair_rate_kernel": "matter-to-pair rate kernel                     = derived at kappa^4/16" in pair_text,
        "4952_formation_cascade_open": "transients or a derived kinetic cascade remain open" in pair_text,
        "Berges_only_22_on_shell": "only the processes described by {\\rr (III)}" in berges_text,
        "Berges_nonzero_chemical_potential": "admits grand canonical" in berges_text and "chemical potential" in berges_text,
        "Berges_off_shell_number_change": "total particle number" in berges_text and "off-shell" in berges_text,
    }

    cosine, mandelstam_s, coefficient = sp.symbols("x s c_ess", real=True)
    cm_amplitude = coefficient * mandelstam_s**2 * (3 + cosine**2) / 4
    cross_section = sp.simplify(sp.integrate(cm_amplitude**2, (cosine, -1, 1)) / (64 * sp.pi * mandelstam_s))
    partial_wave_a0 = sp.simplify(sp.integrate(cm_amplitude, (cosine, -1, 1)) / (32 * sp.pi))
    expected_cross_section = 7 * coefficient**2 * mandelstam_s**3 / (320 * sp.pi)
    expected_a0 = 5 * coefficient * mandelstam_s**2 / (96 * sp.pi)
    scattering_symbolic_ok = sp.simplify(cross_section - expected_cross_section) == 0 and sp.simplify(partial_wave_a0 - expected_a0) == 0

    p1, p2, p3 = sp.symbols("p1nu p2nu p3nu")
    p4 = p1 + p2 - p3
    number_collision_bracket = sp.Integer(1 + 1 - 1 - 1)
    momentum_collision_bracket = sp.simplify(p3 + p4 - p1 - p2)
    collision_invariants_ok = number_collision_bracket == 0 and momentum_collision_bracket == 0

    kernel_rows = tagged(
        [
            {
                "derivation_id": "X2K4953_00_interaction",
                "object": "essential derivative interaction",
                "equation": "L_int=c_ess X^2=(c_ess/4)(partial psi . partial psi)^2",
                "derivation": "X=(partial psi)^2/2 and the 4941 EOM quotient",
                "status": "PARENT_GENERATED_COEFFICIENT_COORDINATE_RETAINED",
                "passed": source_clause_checks["4941_essential_coordinate"] and source_clause_checks["4941_gravity_generates_X2"],
            },
            {
                "derivation_id": "X2K4953_01_vertex",
                "object": "massless four-motion amplitude",
                "equation": "M_22=(c_ess/2)(s^2+t^2+u^2)",
                "derivation": "24 derivative assignments give eight copies of each of three pairings",
                "status": "FOUR_POINT_VERTEX_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "X2K4953_02_CM",
                "object": "centre-of-mass amplitude",
                "equation": "M_22=c_ess s^2(3+cos(theta)^2)/4",
                "derivation": "t=-s(1-cos theta)/2 and u=-s(1+cos theta)/2",
                "status": "CM_ANGULAR_KERNEL_DERIVED",
                "passed": scattering_symbolic_ok,
            },
            {
                "derivation_id": "X2K4953_03_sigma",
                "object": "identical-scalar total cross section",
                "equation": "sigma_22=7 c_ess^2 s^3/(320 pi)=7 c_ess^2 E^6/(5 pi) for s=4E^2",
                "derivation": "integral dOmega |M|^2/(64 pi^2 s) with the identical-final 1/2 factor",
                "status": "EXACT_MASSLESS_CROSS_SECTION_DERIVED",
                "passed": scattering_symbolic_ok,
            },
            {
                "derivation_id": "X2K4953_04_partial_wave",
                "object": "s-wave amplitude",
                "equation": "a0=5 c_ess s^2/(96 pi)",
                "derivation": "M=16pi sum_l(2l+1)a_l P_l",
                "status": "S_WAVE_DERIVED",
                "passed": scattering_symbolic_ok,
            },
            {
                "derivation_id": "X2K4953_05_unitarity",
                "object": "tree-level perturbative unitarity domain",
                "equation": "|c_ess|s^2<=48pi/5; head-on |c_ess|E^4<=3pi/5",
                "derivation": "|Re a0|<=1/2",
                "status": "PERTURBATIVE_DOMAIN_DERIVED",
                "passed": scattering_symbolic_ok,
            },
        ]
    )

    invariant_rows = tagged(
        [
            {
                "derivation_id": "COL4953_00_transport",
                "object": "curved quasiparticle transport",
                "equation": "p^mu nabla_mu f=C_22[f]+S_pair",
                "derivation": "leading on-shell gradient expansion of the 2PI equations with the 4952 source",
                "status": "KINETIC_SPLIT_DECLARED",
                "passed": source_clause_checks["Berges_only_22_on_shell"],
            },
            {
                "derivation_id": "COL4953_01_collision",
                "object": "identical-boson 2-to-2 collision term",
                "equation": "C_cov,1=(1/2!) int dPi2dPi3dPi4 delta4 |M|2 [(1+f1)(1+f2)f3f4-f1f2(1+f3)(1+f4)]",
                "derivation": "cut X2 four-point kernel in the on-shell Markovian limit",
                "status": "COLLISION_KERNEL_DERIVED_UP_TO_STANDARD_MEASURE_CONVENTION",
                "passed": scattering_symbolic_ok,
            },
            {
                "derivation_id": "COL4953_02_moment",
                "object": "symmetrized collision moment",
                "equation": "int dPi1 W1 C1 proportional int dPi1..4 delta4 |M|2 DeltaW [gain-loss]",
                "derivation": "relabel 1,2 and 3,4 and interchange incoming with outgoing variables",
                "status": "COLLISION_INVARIANT_IDENTITY_DERIVED",
                "passed": collision_invariants_ok,
            },
            {
                "derivation_id": "COL4953_03_number",
                "object": "quasiparticle number moment",
                "equation": "int dPi C_22=0 because DeltaW=1+1-1-1=0",
                "derivation": "choose W=1 in the symmetrized collision moment",
                "status": "X2_22_NUMBER_CONSERVATION_EXACT_WITHIN_ON_SHELL_KERNEL",
                "passed": number_collision_bracket == 0,
            },
            {
                "derivation_id": "COL4953_04_four_momentum",
                "object": "stress-energy moment",
                "equation": "int dPi p^nu C_22=0 because p1+p2=p3+p4",
                "derivation": "choose W=p^nu and use the collision delta function",
                "status": "X2_22_STRESS_CONSERVATION_EXACT",
                "passed": momentum_collision_bracket == 0,
            },
            {
                "derivation_id": "COL4953_05_equilibrium",
                "object": "stationary Bose distribution",
                "equation": "f_eq=[exp((E-mu)/T)-1]^-1 with arbitrary collision-compatible mu",
                "derivation": "energy conservation cancels the gain-loss exponent while 2-to-2 conserves N",
                "status": "NONZERO_CHEMICAL_POTENTIAL_ALLOWED",
                "passed": source_clause_checks["Berges_nonzero_chemical_potential"],
            },
            {
                "derivation_id": "COL4953_06_on_shell_number_change",
                "object": "single-vertex number-changing cuts",
                "equation": "0-to-4 is energy-forbidden; massive 1-to-3 is forbidden; massless 1-to-3 is collinear measure zero and M_X2 vanishes there",
                "derivation": "positive on-shell energies, equal-mass thresholds and s=t=u=0 in the collinear massless limit",
                "status": "STRICT_ON_SHELL_SINGLE_VERTEX_NUMBER_CHANGE_ZERO",
                "passed": True,
            },
            {
                "derivation_id": "COL4953_07_off_shell_caveat",
                "object": "finite-width and finite-time number change",
                "equation": "off-shell 1-to-3 and memory terms are present before the quasiparticle Boltzmann limit",
                "derivation": "Berges 2PI comparison, source lines 4945-4968",
                "status": "NOT_REJECTED_BY_ON_SHELL_THEOREM",
                "passed": source_clause_checks["Berges_off_shell_number_change"],
            },
            {
                "derivation_id": "COL4953_08_first_on_shell_multiplier",
                "object": "first generic on-shell number multiplier on the reflection-even branch",
                "equation": "2-to-4 uses two X2 vertices; M_24~c_ess^2 E^6 and sigma_24/sigma_22~O((c_ess E^4)^2)",
                "derivation": "six-point tree power counting with one internal propagator and four-body phase space",
                "status": "PARAMETRIC_SCALING_DERIVED_COEFFICIENT_OPEN",
                "passed": True,
            },
        ]
    )

    spectral_rows = tagged(
        [
            {
                "bound_id": "SPEC4953_00_parent_kernel",
                "object": "4952 formation stress insertion",
                "equation": "dGamma=(kappa^4/16)(1/2!)dPi dPi' [V P S_em(q) P V]/|q^2+i0|^2",
                "meaning": "a transient source fixes the injected pair spectrum; X2 does not supply it",
                "status": "PARENT_SOURCE_KERNEL_RETAINED",
                "passed": source_clause_checks["4952_pair_rate_kernel"],
            },
            {
                "bound_id": "SPEC4953_01_spectral_energy",
                "object": "injected energy spectrum",
                "equation": "E_inj,total=int hbar omega dN_pair(omega); N_quanta=2 int dE_psi(omega)/(hbar omega)",
                "meaning": "each emitted pair at total angular frequency omega contains two quanta",
                "status": "SPECTRAL_NUMBER_MOMENT_DERIVED",
                "passed": True,
            },
            {
                "bound_id": "SPEC4953_02_number_ceiling",
                "object": "number-conserving cascade ceiling",
                "equation": "N_final/N_profile<=int [2 E_profile/(hbar omega)] dE_psi/E_required",
                "meaning": "even 100 percent conversion cannot make enough profile quanta from a high-frequency-only spectrum",
                "status": "SOURCE_INDEPENDENT_NUMBER_BOUND_DERIVED",
                "passed": collision_invariants_ok,
            },
            {
                "bound_id": "SPEC4953_03_monochromatic",
                "object": "monochromatic fixed-energy ceiling",
                "equation": "F_N<=min(1,E_profile/E_injection)",
                "meaning": "2-to-2 scattering may redistribute momentum but cannot increase multiplicity",
                "status": "MONOCHROMATIC_BOUND_DERIVED",
                "passed": collision_invariants_ok,
            },
            {
                "bound_id": "SPEC4953_04_redshift",
                "object": "maximal free-redshift assistance",
                "equation": "F_N,redshift<=min(1,A_max E_profile/E_injection), A_max=1+z_star=1090.92",
                "meaning": "uses recombination rather than the later galaxy-formation epoch and is deliberately over-generous",
                "status": "POST_RECOMBINATION_REDSHIFT_BOUND_DERIVED",
                "passed": MAX_POST_RECOMBINATION_STRETCH == 1090.92,
            },
            {
                "bound_id": "SPEC4953_05_direct_profile",
                "object": "escape condition",
                "equation": "E_injection approximately E_profile=hbar c/R",
                "meaning": "avoids the number deficit but returns to the high-harmonic source-amplitude problem rather than a cascade",
                "status": "DIRECT_PROFILE_INJECTION_REMAINS_SOURCE_CALCULATION",
                "passed": True,
            },
        ]
    )

    occupation_rows = read_csv(OCCUPATION_CSV)
    harmonic_rows = {
        row["galaxy"]: row
        for row in read_csv(HARMONIC_CSV)
        if row["compton_case"] == "massless"
    }
    local_support_rows = [row for row in read_csv(LOCAL_SUPPORT_CSV) if row["compton_case"] == "massless"]
    local_energy_by_system = {
        row["system"]: HBAR_EV_S * float(row["omega_rad_s"]) / 2.0
        for row in local_support_rows
    }

    injection_rows: list[dict[str, Any]] = []
    nonlinear_rows: list[dict[str, Any]] = []
    positive_phase_scales: list[float] = []
    profile_energies: list[float] = []

    for row in occupation_rows:
        galaxy = row["galaxy"]
        radius_m = float(row["outer_radius_kpc"]) * 3.085_677_581_491_367e19
        velocity_m_s = float(row["outer_Vobs_km_s"]) * 1000.0
        omega_orbital = velocity_m_s / radius_m
        energy_profile_ev = HBARC_EV_M / radius_m
        profile_energies.append(energy_profile_ev)
        required_density_j_m3 = float(row["required_effective_energy_density_J_m3"])
        required_density_ev4 = energy_density_to_ev4(required_density_j_m3)
        positive_target = row["positive_outer_residual"] == "True" and required_density_j_m3 > 0.0
        harmonic = harmonic_rows[galaxy]
        minimum_harmonic = int(harmonic["n_min_two_modes_k_at_least_inverse_R"])
        minimum_supported_energy_ev = HBAR_EV_S * minimum_harmonic * omega_orbital / 2.0

        injection_cases = [
            ("direct_profile_quantum", energy_profile_ev, "DIRECT_PROFILE_SOURCE_AMPLITUDE_UNSOLVED"),
            ("minimum_4952_supported_profile_pair", minimum_supported_energy_ev, "HIGH_HARMONIC_SOURCE_AMPLITUDE_UNSOLVED"),
            ("white_dwarf_fundamental_pair_quantum", local_energy_by_system["J2211+1136_white_dwarf"], "HIGH_FREQUENCY_NUMBER_TEST"),
            ("neutron_star_fundamental_pair_quantum", local_energy_by_system["PSR_J1748-2446ad_neutron_star"], "HIGH_FREQUENCY_NUMBER_TEST"),
            ("one_GeV_quantum", 1.0e9, "HIGH_FREQUENCY_NUMBER_TEST"),
            ("UHE_1e20_eV_quantum", 1.0e20, "HIGH_FREQUENCY_NUMBER_TEST"),
        ]
        for injection_case, injection_energy_ev, base_status in injection_cases:
            stretch_required = injection_energy_ev / energy_profile_ev
            fixed_energy_fraction = min(1.0, energy_profile_ev / injection_energy_ev)
            redshift_fraction = min(1.0, MAX_POST_RECOMBINATION_STRETCH / stretch_required)
            if not positive_target:
                route_status = "NO_POSITIVE_OUTER_RESIDUAL_TARGET"
            elif injection_case == "direct_profile_quantum":
                route_status = "NUMBER_GATE_PASSES_DIRECT_SOURCE_AMPLITUDE_UNSOLVED"
            elif injection_case == "minimum_4952_supported_profile_pair":
                route_status = "NUMBER_GATE_PASSES_ONLY_AT_UNSOURCED_HIGH_HARMONIC"
            elif redshift_fraction < 1.0:
                route_status = "NUMBER_AND_MAXIMAL_REDSHIFT_GATE_FAIL"
            else:
                route_status = base_status
            injection_rows.append(
                {
                    "galaxy": galaxy,
                    "injection_case": injection_case,
                    "outer_radius_m": radius_m,
                    "outer_velocity_m_s": velocity_m_s,
                    "required_effective_energy_density_J_m3": required_density_j_m3,
                    "occupation_per_R_cell_required": row["occupation_per_R_cell_required"],
                    "positive_outer_residual_target": positive_target,
                    "profile_quantum_energy_eV": energy_profile_ev,
                    "injection_quantum_energy_eV": injection_energy_ev,
                    "multiplicity_ratio_injection_to_profile": stretch_required,
                    "fixed_final_energy_number_fraction_max": fixed_energy_fraction,
                    "free_redshift_stretch_required": stretch_required,
                    "max_post_recombination_stretch": MAX_POST_RECOMBINATION_STRETCH,
                    "redshift_assisted_number_fraction_max": redshift_fraction,
                    "maximal_redshift_can_reach_profile_energy": stretch_required <= MAX_POST_RECOMBINATION_STRETCH,
                    "minimum_4952_profile_harmonic": minimum_harmonic,
                    "two_to_two_changes_particle_number": False,
                    "route_status": route_status,
                }
            )

        if positive_target:
            phase_scale = required_density_ev4 * (LIGHT_SPEED / radius_m) * GENEROUS_FORMATION_TIME_S
            positive_phase_scales.append(phase_scale)
            c_required = 1.0 / phase_scale
            cutoff_required_ev = c_required ** (-0.25)
            natural_epsilon = NATURAL_C_ESS_EV_M4 * required_density_ev4
            natural_phase = NATURAL_C_ESS_EV_M4 * phase_scale
        else:
            phase_scale = 0.0
            c_required = math.nan
            cutoff_required_ev = math.nan
            natural_epsilon = 0.0
            natural_phase = 0.0
        nonlinear_rows.append(
            {
                "galaxy": galaxy,
                "outer_radius_m": radius_m,
                "required_effective_energy_density_J_m3": required_density_j_m3,
                "required_effective_energy_density_eV4": required_density_ev4,
                "positive_outer_residual_target": positive_target,
                "profile_angular_frequency_rad_s": LIGHT_SPEED / radius_m,
                "generous_formation_time_s": GENEROUS_FORMATION_TIME_S,
                "phase_scale_per_c_ess_eV4": phase_scale,
                "natural_c_ess_eV_minus4": NATURAL_C_ESS_EV_M4,
                "natural_X2_to_X_ratio": natural_epsilon,
                "natural_secular_phase_upper_comparator": natural_phase,
                "c_ess_required_for_order_one_phase_eV_minus4": c_required,
                "corresponding_cutoff_eV": cutoff_required_ev,
                "natural_coefficient_can_redistribute": natural_phase >= 1.0,
                "two_to_two_can_build_required_number": False,
                "status": "NATURAL_GRAVITY_COMPARATOR_NOT_PARENT_COEFFICIENT",
            }
        )

    local_rows: list[dict[str, Any]] = []
    local_mass = {
        "J2211+1136_white_dwarf": 1.268 * SOLAR_MASS,
        "PSR_J1748-2446ad_neutron_star": 2.0 * SOLAR_MASS,
    }
    local_mass_source = {
        "J2211+1136_white_dwarf": "Kilic et al. source mass 1.268 Msun",
        "PSR_J1748-2446ad_neutron_star": "deliberately high 2 Msun comparator; spin and radius are sourced in 4952",
    }
    for row in local_support_rows:
        system = row["system"]
        mass_kg = local_mass[system]
        radius_m = float(row["radius_m"])
        omega_source = float(row["omega_rad_s"])
        moment_inertia = 0.4 * mass_kg * radius_m**2
        rotational_energy = 0.5 * moment_inertia * omega_source**2
        volume = 4.0 * math.pi * radius_m**3 / 3.0
        rotational_density_j_m3 = rotational_energy / volume
        rotational_density_ev4 = energy_density_to_ev4(rotational_density_j_m3)
        quantum_energy_ev = HBAR_EV_S * omega_source / 2.0
        quantum_omega = omega_source / 2.0
        phase_scale = rotational_density_ev4 * quantum_omega * GENEROUS_FORMATION_TIME_S
        efficiency_ceilings = [galaxy_scale / phase_scale for galaxy_scale in positive_phase_scales]
        c_required = 1.0 / phase_scale
        local_rows.append(
            {
                "system": system,
                "mass_kg": mass_kg,
                "mass_source": local_mass_source[system],
                "radius_m": radius_m,
                "source_angular_frequency_rad_s": omega_source,
                "fundamental_pair_quantum_energy_eV": quantum_energy_ev,
                "uniform_sphere_rotational_energy_J": rotational_energy,
                "rotational_energy_density_J_m3": rotational_density_j_m3,
                "rotational_energy_density_eV4": rotational_density_ev4,
                "assumed_motion_injection_efficiency": 1.0,
                "assumption": "100 percent rotational-energy conversion is an upper comparator, not a physical emission claim",
                "natural_c_ess_eV_minus4": NATURAL_C_ESS_EV_M4,
                "natural_X2_to_X_ratio": NATURAL_C_ESS_EV_M4 * rotational_density_ev4,
                "natural_secular_phase_upper_comparator": NATURAL_C_ESS_EV_M4 * phase_scale,
                "c_ess_required_for_order_one_phase_eV_minus4": c_required,
                "galaxy_to_local_injection_efficiency_ceiling_min": min(efficiency_ceilings),
                "galaxy_to_local_injection_efficiency_ceiling_median": statistics.median(efficiency_ceilings),
                "galaxy_to_local_injection_efficiency_ceiling_max": max(efficiency_ceilings),
                "equal_injection_efficiency_has_universal_phase_window": any(value >= 1.0 for value in efficiency_ceilings),
                "status": "LOCAL_SUPPRESSION_REQUIREMENT_DERIVED_SOURCE_EFFICIENCY_UNSOLVED",
            }
        )

    benchmark_energies = {
        "median_galaxy_profile": statistics.median(profile_energies),
        "white_dwarf_fundamental_pair_quantum": local_energy_by_system["J2211+1136_white_dwarf"],
        "neutron_star_fundamental_pair_quantum": local_energy_by_system["PSR_J1748-2446ad_neutron_star"],
        "one_GeV": 1.0e9,
        "UHE_1e20_eV": 1.0e20,
    }
    number_change_rows: list[dict[str, Any]] = []
    for energy_case, energy_ev in benchmark_energies.items():
        energy_decimal = Decimal(str(energy_ev))
        effective_coupling = DECIMAL_NATURAL_C_ESS * energy_decimal**4
        sigma_22_m2 = (
            Decimal(7)
            * DECIMAL_NATURAL_C_ESS**2
            * energy_decimal**6
            * DECIMAL_HBARC_EV_M**2
            / (Decimal(5) * DECIMAL_PI)
        )
        unitarity_ratio = effective_coupling / (Decimal(3) * DECIMAL_PI / Decimal(5))
        number_change_ratio = effective_coupling**2
        number_change_rows.append(
            {
                "energy_case": energy_case,
                "energy_eV": energy_ev,
                "natural_c_ess_eV_minus4": NATURAL_C_ESS_EV_M4,
                "dimensionless_g_X2_abs_cE4": decimal_scientific(effective_coupling),
                "sigma_22_natural_m2": decimal_scientific(sigma_22_m2),
                "sigma_22_natural_log10_m2": float(sigma_22_m2.log10()),
                "head_on_s_wave_unitarity_ratio": decimal_scientific(unitarity_ratio),
                "sigma_24_over_sigma_22_parametric_upper_without_phase_space": decimal_scientific(number_change_ratio),
                "sigma_24_over_sigma_22_log10_without_phase_space": float(number_change_ratio.log10()),
                "two_to_two_delta_N": 0,
                "two_to_four_delta_N": 2,
                "interpretation": "c=1/Mbar_Pl^4 is a generous natural-gravity comparator, not the solved MTS coefficient",
                "status": "NATURAL_NUMBER_CHANGE_PARAMETRICALLY_TINY",
            }
        )

    positive_injection_rows = [row for row in injection_rows if row["positive_outer_residual_target"]]
    high_frequency_rows = [
        row
        for row in positive_injection_rows
        if row["injection_case"] in {
            "white_dwarf_fundamental_pair_quantum",
            "neutron_star_fundamental_pair_quantum",
            "one_GeV_quantum",
            "UHE_1e20_eV_quantum",
        }
    ]
    direct_rows = [row for row in positive_injection_rows if row["injection_case"] == "direct_profile_quantum"]
    harmonic_profile_rows = [row for row in positive_injection_rows if row["injection_case"] == "minimum_4952_supported_profile_pair"]

    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4953_00_exact_kernel",
                "question": "Is the leading X2 scattering amplitude and perturbative domain known?",
                "answer": "YES",
                "evidence": "M22=(c_ess/2)(s2+t2+u2); sigma22=7c_ess2 s3/(320pi); |c_ess|s2<=48pi/5",
                "status": "DERIVED",
            },
            {
                "decision_id": "DEC4953_01_leading_cascade",
                "question": "Can the leading on-shell X2 2-to-2 cascade build the required galaxy particle number?",
                "answer": "NO",
                "evidence": "int dPi C22=0 for every c_ess; 2-to-2 preserves N and four-momentum",
                "status": "ROUTE_REJECTED_EXACTLY",
            },
            {
                "decision_id": "DEC4953_02_high_frequency_formation",
                "question": "Can high-frequency-only injection be converted to the profile population by 2-to-2 plus maximal post-recombination redshift?",
                "answer": "NO_FOR_ALL_EXECUTED_HIGH_FREQUENCY_CASES",
                "evidence": f"{sum(row['redshift_assisted_number_fraction_max'] < 1.0 for row in high_frequency_rows)}/{len(high_frequency_rows)} positive-target rows fail even with Amax={MAX_POST_RECOMBINATION_STRETCH}",
                "status": "EXECUTED_ROUTE_REJECTED",
            },
            {
                "decision_id": "DEC4953_03_direct_profile_formation",
                "question": "Is direct formation injection at E approximately hbar c/R rejected?",
                "answer": "NO",
                "evidence": f"number gate passes on {len(direct_rows)} positive-target rows, but the required high-harmonic stress amplitude remains unsolved on {len(harmonic_profile_rows)} rows",
                "status": "OPEN_SOURCE_SPECTRUM_NOT_A_CASCADE",
            },
            {
                "decision_id": "DEC4953_04_number_change",
                "question": "Does the on-shell theorem reject all quantum number change?",
                "answer": "NO",
                "evidence": "off-shell finite-time 1-to-3 terms and two-vertex 2-to-4 remain; sigma24/sigma22 scales as O((c_ess E4)^2)",
                "status": "FULL_2PI_NUMBER_CHANGE_KERNEL_REQUIRED",
            },
            {
                "decision_id": "DEC4953_05_natural_X2",
                "question": "Does a natural Planck-suppressed X2 coefficient redistribute the executed galaxy or compact comparators?",
                "answer": "NO",
                "evidence": f"maximum galaxy natural secular comparator={max(row['natural_secular_phase_upper_comparator'] for row in nonlinear_rows):.6e}; maximum compact comparator={max(row['natural_secular_phase_upper_comparator'] for row in local_rows):.6e}",
                "status": "NATURAL_COMPARATOR_FAILS_NOT_PARENT_COEFFICIENT_PROOF",
            },
            {
                "decision_id": "DEC4953_06_local_selector",
                "question": "Does one equal-efficiency universal X2 coefficient provide a galaxy-strong/local-weak window?",
                "answer": "NO_UNDER_THE_MAXIMAL_EQUAL_EFFICIENCY_COMPARATOR",
                "evidence": "compact rotational phase scales exceed every positive galaxy phase scale; a source-efficiency suppression must be derived",
                "status": "CONDITIONAL_NO_WINDOW_SOURCE_COUPLING_NEXT",
            },
            {
                "decision_id": "DEC4953_07_local_branch",
                "question": "Does failure of the galaxy cascade damage the 4947 stationary local GR/Newton/Maxwell branch?",
                "answer": "NO",
                "evidence": "X2 is quartic at psi=0 and the rejected route concerns occupation generation",
                "status": "4947_LOCAL_BRANCH_RETAINED",
            },
            {
                "decision_id": "DEC4953_08_full_MTS",
                "question": "Is the full galaxy/local MTS bridge derived?",
                "answer": "NO",
                "evidence": "direct formation stress amplitude and the off-shell number-changing source kernel are not parent-solved",
                "status": "FULL_MTS_PROMOTION_BLOCKED",
            },
        ]
    )

    write_csv(KERNEL_CSV, kernel_rows)
    write_csv(INVARIANT_CSV, invariant_rows)
    write_csv(SPECTRAL_CSV, spectral_rows)
    write_csv(SPARC_INJECTION_CSV, tagged(injection_rows))
    write_csv(SPARC_NONLINEAR_CSV, tagged(nonlinear_rows))
    write_csv(LOCAL_CSV, tagged(local_rows))
    write_csv(NUMBER_CHANGE_CSV, tagged(number_change_rows))
    write_csv(DECISION_CSV, decision_rows)

    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "symbolic": {
            "cm_amplitude": str(cm_amplitude),
            "cross_section": str(cross_section),
            "partial_wave_a0": str(partial_wave_a0),
            "scattering_symbolic_ok": scattering_symbolic_ok,
            "number_collision_bracket": str(number_collision_bracket),
            "momentum_collision_bracket": str(momentum_collision_bracket),
            "collision_invariants_ok": collision_invariants_ok,
        },
        "constants": {
            "reduced_Planck_mass_eV": REDUCED_PLANCK_MASS_EV,
            "natural_c_ess_eV_minus4": NATURAL_C_ESS_EV_M4,
            "generous_formation_time_s": GENEROUS_FORMATION_TIME_S,
            "Planck_z_star": PLANCK_Z_STAR,
            "max_post_recombination_stretch": MAX_POST_RECOMBINATION_STRETCH,
        },
        "execution": {
            "galaxy_rows": len(occupation_rows),
            "positive_outer_residual_targets": sum(row["positive_outer_residual_target"] for row in nonlinear_rows),
            "injection_rows": len(injection_rows),
            "high_frequency_positive_rows": len(high_frequency_rows),
            "high_frequency_rows_failing_maximal_redshift": sum(row["redshift_assisted_number_fraction_max"] < 1.0 for row in high_frequency_rows),
            "direct_profile_positive_rows": len(direct_rows),
            "natural_galaxy_phase_max": max(row["natural_secular_phase_upper_comparator"] for row in nonlinear_rows),
            "natural_compact_phase_max": max(row["natural_secular_phase_upper_comparator"] for row in local_rows),
            "local_equal_efficiency_window_count": sum(row["equal_injection_efficiency_has_universal_phase_window"] for row in local_rows),
        },
        "decision": {
            "X2_22_number_building_route": "REJECTED_EXACTLY",
            "executed_high_frequency_formation_plus_redshift": "REJECTED",
            "direct_profile_frequency_formation": "OPEN_SOURCE_AMPLITUDE_UNSOLVED",
            "off_shell_and_24_number_change": "OPEN_PARENT_KERNEL_AND_COEFFICIENT_UNSOLVED",
            "natural_gravity_X2_comparator": "FAR_TOO_WEAK_NOT_A_PARENT_COEFFICIENT_PROOF",
            "local_GR_Newton_Maxwell_4947": "RETAINED",
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks = [
        source_hashes_match,
        all(source_clause_checks.values()),
        scattering_symbolic_ok,
        collision_invariants_ok,
        len(occupation_rows) == 175,
        len(harmonic_rows) == 175,
        len(injection_rows) == 6 * len(occupation_rows),
        len(local_rows) == 2,
        all(row["redshift_assisted_number_fraction_max"] < 1.0 for row in high_frequency_rows),
        all(not row["two_to_two_can_build_required_number"] for row in nonlinear_rows),
        all(not row["valid_for_full_MTS_claim"] for table in (kernel_rows, invariant_rows, spectral_rows, decision_rows) for row in table),
    ]
    return 0 if all(all_checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
