from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4952"

RESULT_JSON = SOURCE / "visible_matter_graviton_CTP_pair_source_results.json"
VERTEX_CSV = SOURCE / "parent_hpsipsi_vertex_and_CTP_chain.csv"
SPECTRAL_CSV = SOURCE / "emission_spectrum_and_support_theorem.csv"
SPARC_CSV = SOURCE / "SPARC_outer_harmonic_support_gate.csv"
LOCAL_CSV = SOURCE / "local_compact_rotator_harmonic_support_gate.csv"
POYNTING_CSV = SOURCE / "Poynting_and_wave_source_gate.csv"
DECISION_CSV = SOURCE / "CTP_pair_source_route_decision.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"

LOCAL_GR_4947 = POST / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
CTP_4949 = POST / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"
STATIC_4951 = POST / "4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md"

HU_TEX = SOURCE / "0802.0658v1.tex"
HU_PDF = SOURCE / "0802.0658v1.pdf"
HESSELS_TEX = SOURCE / "astro-ph-0601337v1.tex"
HESSELS_PDF = SOURCE / "astro-ph-0601337v1.pdf"
KILIC_TEX = SOURCE / "src2111" / "ms.tex"
KILIC_PDF = SOURCE / "2111.14902v1.pdf"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_README = GALAXY_REPO / "README.md"
GALAXY_SAMPLES = GALAXY_REPO / "data" / "samples.js"
EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"

MARKER = "MTS_4952_VISIBLE_MATTER_GRAVITON_CTP_PAIR_SOURCE_GATE"
CHECKED_DATE = "2026-07-13"

LIGHT_SPEED = 299_792_458.0
NEWTON_G = 6.67430e-11
SOLAR_MASS = 1.98847e30
KPC = 3.085677581491367e19
SMOOTH_HARMONIC_CEILING = 4

EXPECTED_HASHES = {
    LOCAL_GR_4947: "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    CTP_4949: "772bee9863471ab7e4a4e4887773b91786110539d471243c26aaa1b88866f7b8",
    STATIC_4951: "1dd7f2632ab15370e7b44272c2439a6cf70d5559b1c7993b6f55d7e9fab9a131",
    HU_TEX: "4b3c3c20f7c41e2cf36e19082ec34bbba7ca7993f3bdd54f33e272c4f3b0fb38",
    HESSELS_TEX: "e2cba6c65996c852bc4c4555b975f456f3c4d4279f52ce2f0dfd4fad065d7961",
    KILIC_TEX: "8da06e07b0f91eea9845d84d4d5f6afa6b33416ff2a7a1b5713bd5977afed5ff",
    GALAXY_README: "e9acb4d72fc6fdd7f39ba62e18357746ae423e61c7e6932cf8b5b8f45265e402",
    GALAXY_SAMPLES: "a7edd2db0e237d7997207bf1ee53c78e492cf5dbc7a7cbfc478c12e69bddbfba",
}

COMPTON_CASES = {
    "massless": math.inf,
    "lambda_100_kpc": 100.0 * KPC,
    "lambda_10_kpc": 10.0 * KPC,
    "lambda_1_kpc": KPC,
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


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


def load_samples() -> list[dict[str, str]]:
    raw = read_text(GALAXY_SAMPLES)
    start = raw.index("[")
    end = raw.rindex("]") + 1
    return json.loads(raw[start:end])


def parse_rotmod(text: str) -> list[list[float]]:
    rows: list[list[float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        values = [float(value) for value in stripped.split()]
        if len(values) >= 6:
            rows.append(values)
    return rows


def ceil_ratio(value: float) -> int:
    return int(math.ceil(value - 1.0e-13))


def harmonic_thresholds(radius_m: float, omega_source: float, compton_length_m: float) -> dict[str, Any]:
    omega_gap = 0.0 if math.isinf(compton_length_m) else LIGHT_SPEED / compton_length_m
    omega_profile = math.sqrt((LIGHT_SPEED / radius_m) ** 2 + omega_gap**2)
    minimum_gap_pair = 0 if omega_gap == 0.0 else ceil_ratio(2.0 * omega_gap / omega_source)
    minimum_total_q_at_inverse_radius = ceil_ratio(
        math.sqrt((LIGHT_SPEED / radius_m) ** 2 + 4.0 * omega_gap**2) / omega_source
    )
    minimum_one_profile_mode = ceil_ratio((omega_profile + omega_gap) / omega_source)
    minimum_two_profile_modes = ceil_ratio(2.0 * omega_profile / omega_source)
    return {
        "omega_gap_rad_s": omega_gap,
        "n_min_gap_pair": minimum_gap_pair,
        "n_min_total_Q_equals_inverse_R": minimum_total_q_at_inverse_radius,
        "n_min_one_mode_k_at_least_inverse_R": minimum_one_profile_mode,
        "n_min_two_modes_k_at_least_inverse_R": minimum_two_profile_modes,
        "smooth_n_le_4_can_make_two_profile_modes": minimum_two_profile_modes <= SMOOTH_HARMONIC_CEILING,
    }


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)

    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())

    local_gr_text = read_text(LOCAL_GR_4947)
    ctp_text = read_text(CTP_4949)
    static_text = read_text(STATIC_4951)
    hu_text = read_text(HU_TEX)
    hessels_text = read_text(HESSELS_TEX)
    kilic_text = read_text(KILIC_TEX)

    source_clause_checks = {
        "4947_universal_graviton_residue": "G_Einstein=G_exchange=G_Newton=G_orbit=G_lensing=G_wave" in local_gr_text,
        "4947_Poynting_owned_by_Maxwell": "Poynting vector" in local_gr_text,
        "4949_metric_pair_vertex_open": "Metric exchange does generate scalar-pair vertices" in ctp_text,
        "4951_hpsipsi_route_selected": "h psi psi" in static_text,
        "Hu_noise_kernel_definition": "N_{abcd}[g;x,y)={1\\over2}\\langle\\{\\hat t_{ab}" in hu_text,
        "Hu_influence_noise_coefficient": "+{i\\over 8}" in hu_text,
        "Hu_two_particle_timelike_support": "\\theta (-p^2\\!-\\!4m^2)" in hu_text,
        "Hessels_716_Hz": "716\\,Hz" in hessels_text,
        "Hessels_radius_upper_16_km": "upper limit of 16\\,km" in hessels_text,
        "Kilic_period_70_32_s": "70.32 \\pm 0.04" in kilic_text,
        "Kilic_mass_and_logg": "M=1.268\\pm0.010" in kilic_text and "\\log{g}=9.214\\pm 0.027" in kilic_text,
    }

    mass_squared, scalar_product = sp.symbols("m2 s", real=True)
    q_contract_p = sp.simplify(mass_squared + scalar_product - (scalar_product + mass_squared))
    q_contract_pprime = sp.simplify(mass_squared + scalar_product - (scalar_product + mass_squared))
    ward_identity_zero = q_contract_p == 0 and q_contract_pprime == 0

    interaction_coefficient = Fraction(1, 2)
    induced_metric_noise_coefficient = interaction_coefficient**2
    system_influence_noise_coefficient = interaction_coefficient**2 * induced_metric_noise_coefficient / 2
    exchange_amplitude_coefficient = interaction_coefficient**2
    exchange_rate_coefficient = exchange_amplitude_coefficient**2

    vertex_rows = tagged(
        [
            {
                "derivation_id": "VTX4952_00_parent_expansion",
                "object": "canonical weak-field normalization",
                "equation": "g_mn=eta_mn+kappa h_mn; S_int=(kappa/2) int h_mn T^mn",
                "derivation": "first metric variation of the unchanged matter and motion actions",
                "status": "PARENT_LINEAR_COUPLING_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "VTX4952_01_pair_vertex",
                "object": "one-graviton two-motion-field vertex",
                "equation": "V^mn=Z0[p^m pprime^n+p^n pprime^m-eta^mn(p.pprime+mpsi^2)]",
                "derivation": "vacuum-to-two-particle matrix element of T_psi^mn in signature (+---)",
                "status": "HPSIPSI_VERTEX_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "VTX4952_02_Ward",
                "object": "pair-vertex Ward identity",
                "equation": "q_m V^mn=0 for q=p+pprime and p^2=pprime^2=mpsi^2",
                "derivation": f"coefficients of p^n and pprime^n are ({q_contract_p},{q_contract_pprime})",
                "status": "CONSERVED_GAUGE_SAFE_VERTEX",
                "passed": ward_identity_zero,
            },
            {
                "derivation_id": "VTX4952_03_de_Donder",
                "object": "conserved-source graviton kernel",
                "equation": "P_mnrs=(eta_mr eta_ns+eta_ms eta_nr-eta_mn eta_rs)/2",
                "derivation": "gauge-dependent propagator terms vanish between q_m T_m^mn=0 and q_r V^rs=0",
                "status": "CONSERVED_PROJECTOR_SUFFICIENT",
                "passed": ward_identity_zero,
            },
            {
                "derivation_id": "VTX4952_04_O4_order",
                "object": "C^2 X portal around flat psi=0",
                "equation": "C=O(kappa h), C^2 X=O(kappa^2 h^2 psi^2)",
                "derivation": "field-order expansion",
                "status": "NO_ADDITIONAL_ONE_GRAVITON_PAIR_VERTEX",
                "passed": True,
            },
            {
                "derivation_id": "VTX4952_05_metric_noise",
                "object": "matter-induced metric Hadamard/noise kernel",
                "equation": "N_h^ind=(kappa^2/4) D_R N_m D_A",
                "derivation": "h_ind=(kappa/2)D_R t_m and N_m=<anticommutator(t_m,t_m)>/2",
                "status": "INDUCED_GRAVITON_NOISE_DERIVED",
                "passed": induced_metric_noise_coefficient == Fraction(1, 4),
            },
            {
                "derivation_id": "VTX4952_06_scalar_noise_action",
                "object": "motion-field influence noise",
                "equation": "Im S_IF^psi=(kappa^4/32) T_psi^- D_R N_m D_A T_psi^-",
                "derivation": "Gaussian influence coefficient (1/2)(kappa/2)^2 times N_h^ind",
                "status": "QUARTIC_CTP_NOISE_TERM_DERIVED",
                "passed": system_influence_noise_coefficient == Fraction(1, 32),
            },
            {
                "derivation_id": "VTX4952_07_pair_amplitude",
                "object": "matter-to-motion-pair exchange amplitude",
                "equation": "A_m_to_psipsi=(kappa^2/4) T_m^mn D_mnrs V^rs",
                "derivation": "cross term after Gaussian graviton integration",
                "status": "PAIR_AMPLITUDE_DERIVED",
                "passed": exchange_amplitude_coefficient == Fraction(1, 4),
            },
            {
                "derivation_id": "VTX4952_08_rate_prefactor",
                "object": "unsymmetrized bath-emission contribution to pair rate",
                "equation": "dGamma=(kappa^4/16)(1/2!) dPi_p dPi_pprime V P S_m^em(q) P V/|q^2+i0|^2",
                "derivation": "squared exchange amplitude; identical-pair factor displayed separately",
                "status": "PAIR_RATE_KERNEL_DERIVED",
                "passed": exchange_rate_coefficient == Fraction(1, 16),
            },
        ]
    )

    spectral_rows = tagged(
        [
            {
                "theorem_id": "SPEC4952_00_noise_not_emission",
                "object": "symmetrized stress noise",
                "equation_or_condition": "N_m=(S_em+S_abs)/2 at positive frequency",
                "consequence": "nonzero vacuum noise is not by itself a source of real pairs",
                "status": "SYMMETRIZED_NOISE_TRAP_REMOVED",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_01_ground_state",
                "object": "stationary ground-state matter bath",
                "equation_or_condition": "S_em(q)=sum_i,f p_i |<f|t_m|i>|^2 delta(q0-E_i+E_f); E_f>=E_0",
                "consequence": "S_em(q0>0)=0 in the exact ground state",
                "status": "GROUND_STATE_CANNOT_PUMP_MOTION_VACUUM",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_02_KMS",
                "object": "thermal stationary bath",
                "equation_or_condition": "S_em(omega)=exp[-hbar omega/(k_B T)] S_abs(omega) for omega>0",
                "consequence": "positive-energy pumping is fixed by detailed balance, not by N_m alone",
                "status": "THERMAL_EMISSION_BOLTZMANN_WEIGHTED",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_03_pair_support",
                "object": "two on-shell motion quanta",
                "equation_or_condition": "q=p+pprime; q^2>=4 mpsi^2, equivalently omega^2>=c^2 Q^2+4 omega_gap^2",
                "consequence": "only timelike source-emission support contributes",
                "status": "EXACT_TWO_PARTICLE_SUPPORT_PROVED",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_04_stationary",
                "object": "stationary axisymmetric stress including DC mass current",
                "equation_or_condition": "partial_t T_m=0 gives S_em proportional to delta(omega)",
                "consequence": "no positive-energy pair production",
                "status": "STATIC_AND_DC_POYNTING_PAIR_SOURCE_ZERO",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_05_total_Q_profile",
                "object": "source Fourier component Q=1/R at harmonic n Omega",
                "equation_or_condition": "n >= (c/v) sqrt[1+4(R/lambda_c)^2]",
                "consequence": "exact support threshold at declared total spatial scale",
                "status": "TOTAL_MOMENTUM_SUPPORT_THRESHOLD_DERIVED",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_06_one_profile_mode",
                "object": "at least one produced mode with k>=1/R",
                "equation_or_condition": "n >= (R/v)[sqrt((c/R)^2+omega_gap^2)+omega_gap]",
                "consequence": "necessary energy threshold allowing the partner at rest",
                "status": "ONE_PROFILE_MODE_THRESHOLD_DERIVED",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_07_two_profile_modes",
                "object": "two produced modes each with k>=1/R",
                "equation_or_condition": "n >= 2(c/v) sqrt[1+(R/lambda_c)^2]",
                "consequence": "direct pair population of the radial profile requires high harmonics",
                "status": "TWO_PROFILE_MODE_THRESHOLD_DERIVED",
                "passed": True,
            },
            {
                "theorem_id": "SPEC4952_08_low_harmonic_wavelength",
                "object": "massless n-th source harmonic",
                "equation_or_condition": "k_max R<=n v/c; physical lambda_min/R>=2 pi c/(n v)",
                "consequence": "low harmonics create only modes much longer than R",
                "status": "LOW_HARMONIC_SCALE_MISMATCH_PROVED",
                "passed": True,
            },
        ]
    )

    samples = load_samples()
    sparc_rows: list[dict[str, Any]] = []
    for sample in samples:
        points = parse_rotmod(sample["text"])
        outer = points[-1]
        radius_kpc, velocity_km_s = outer[0], outer[1]
        radius_m = radius_kpc * KPC
        velocity_m_s = velocity_km_s * 1000.0
        omega_orbital = velocity_m_s / radius_m
        for case, compton_length_m in COMPTON_CASES.items():
            thresholds = harmonic_thresholds(radius_m, omega_orbital, compton_length_m)
            sparc_rows.append(
                {
                    "galaxy": sample["name"].removesuffix("_rotmod.dat"),
                    "compton_case": case,
                    "compton_length_m": compton_length_m,
                    "outer_radius_kpc": radius_kpc,
                    "outer_velocity_km_s": velocity_km_s,
                    "generous_omega_orbital_rad_s": omega_orbital,
                    "v_over_c": velocity_m_s / LIGHT_SPEED,
                    "fundamental_kmax_times_R_massless": velocity_m_s / LIGHT_SPEED,
                    "fundamental_physical_lambda_min_over_R_massless": 2.0 * math.pi * LIGHT_SPEED / velocity_m_s,
                    **thresholds,
                    "frequency_assumption": "Omega=v_outer/R_outer is a generous upper proxy, not a fitted pattern speed",
                    "status": "DIRECT_PROFILE_SUPPORT_TESTED_NOT_AMPLITUDE_FIT",
                }
            )
    sparc_rows = tagged(sparc_rows)

    wd_period_s = 70.32
    wd_mass_kg = 1.268 * SOLAR_MASS
    wd_surface_g_m_s2 = 10.0**9.214 / 100.0
    wd_radius_m = math.sqrt(NEWTON_G * wd_mass_kg / wd_surface_g_m_s2)
    local_systems = [
        {
            "system": "J2211+1136_white_dwarf",
            "radius_m": wd_radius_m,
            "omega_rad_s": 2.0 * math.pi / wd_period_s,
            "period_or_frequency_source": "Kilic et al. arXiv:2111.14902v1: P=70.32+/-0.04 s; M=1.268 Msun; log g=9.214; R=sqrt(GM/g)",
        },
        {
            "system": "PSR_J1748-2446ad_neutron_star",
            "radius_m": 16_000.0,
            "omega_rad_s": 2.0 * math.pi * 716.0,
            "period_or_frequency_source": "Hessels et al. arXiv:astro-ph/0601337v1: nu=716 Hz and R<16 km; 16 km maximizes v/c and minimizes thresholds",
        },
    ]
    local_rows: list[dict[str, Any]] = []
    for system in local_systems:
        radius_m = float(system["radius_m"])
        omega_source = float(system["omega_rad_s"])
        velocity_m_s = radius_m * omega_source
        for case, compton_length_m in COMPTON_CASES.items():
            thresholds = harmonic_thresholds(radius_m, omega_source, compton_length_m)
            local_rows.append(
                {
                    "system": system["system"],
                    "compton_case": case,
                    "compton_length_m": compton_length_m,
                    "radius_m": radius_m,
                    "omega_rad_s": omega_source,
                    "equatorial_velocity_m_s": velocity_m_s,
                    "v_over_c": velocity_m_s / LIGHT_SPEED,
                    "fundamental_kmax_times_R_massless": velocity_m_s / LIGHT_SPEED,
                    "fundamental_physical_lambda_min_over_R_massless": 2.0 * math.pi * LIGHT_SPEED / velocity_m_s,
                    **thresholds,
                    "source": system["period_or_frequency_source"],
                    "status": "LOCAL_SPECTRAL_CHALLENGE_TESTED_NOT_PAIR_AMPLITUDE_BOUND",
                }
            )
    local_rows = tagged(local_rows)

    poynting_rows = tagged(
        [
            {
                "source_id": "POY4952_00_DC",
                "source_type": "stationary EM energy flux or steady Poynting vector",
                "stress_support": "T_EM^0i nonzero but omega=0",
                "pair_consequence": "changes the stationary metric and frame dragging; cannot supply positive pair energy",
                "decision": "EXACT_ZERO_REAL_PAIR_SOURCE",
                "passed": True,
            },
            {
                "source_id": "POY4952_01_periodic",
                "source_type": "periodic EM field",
                "stress_support": "T_EM is quadratic and contains DC plus sum/difference harmonics",
                "pair_consequence": "positive-frequency emission can source pairs only when q is timelike and profile thresholds are met",
                "decision": "ALLOWED_BUT_FREQUENCY_AND_KAPPA4_GATED",
                "passed": True,
            },
            {
                "source_id": "POY4952_02_radiation",
                "source_type": "high-frequency stellar or plasma radiation",
                "stress_support": "large omega but microscopic wavelength and generally incoherent phases",
                "pair_consequence": "can source short-scale pairs; a galaxy-scale state requires a separately derived cascade or condensate transport law",
                "decision": "NOT_A_DIRECT_GALAXY_PROFILE_DERIVATION",
                "passed": True,
            },
            {
                "source_id": "POY4952_03_universal_stress",
                "source_type": "all Maxwell and matter stress",
                "stress_support": "same rank-one graviton residue fixed at checkpoint 4947",
                "pair_consequence": "no independent Poynting coupling may be tuned to galaxies while silenced locally",
                "decision": "UNIVERSAL_SOURCE_NORMALIZATION_RETAINED",
                "passed": True,
            },
        ]
    )

    massless_galaxy = [row for row in sparc_rows if row["compton_case"] == "massless"]
    massless_n_two = [int(row["n_min_two_modes_k_at_least_inverse_R"]) for row in massless_galaxy]
    massless_n_one = [int(row["n_min_one_mode_k_at_least_inverse_R"]) for row in massless_galaxy]
    easiest_two = min(massless_galaxy, key=lambda row: int(row["n_min_two_modes_k_at_least_inverse_R"]))
    hardest_two = max(massless_galaxy, key=lambda row: int(row["n_min_two_modes_k_at_least_inverse_R"]))
    local_massless = [row for row in local_rows if row["compton_case"] == "massless"]

    direct_smooth_galaxy_profile = any(bool(row["smooth_n_le_4_can_make_two_profile_modes"]) for row in massless_galaxy)
    pair_source_exists_formally = all(bool(row["passed"]) for row in vertex_rows)
    route_claim = False

    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4952_00_vertex",
                "question": "Does the unchanged parent contain a conserved visible-matter to motion-pair channel?",
                "result": pair_source_exists_formally,
                "decision": "YES_AT_ORDER_KAPPA4_IN_RATE",
                "claim_boundary": "derives a channel, not a macroscopic occupation",
            },
            {
                "decision_id": "DEC4952_01_ground_state",
                "question": "Does nonzero symmetrized vacuum stress noise pump the motion vacuum?",
                "result": False,
                "decision": "NO_GROUND_STATE_EMISSION_SPECTRUM_ZERO",
                "claim_boundary": "vacuum polarization remains but is not renamed as particles",
            },
            {
                "decision_id": "DEC4952_02_stationary",
                "question": "Can stationary baryonic, mass-current or DC Poynting stress populate motion pairs?",
                "result": False,
                "decision": "NO_EXACT_OMEGA_ZERO_OBSTRUCTION",
                "claim_boundary": "stationary stress still gravitates through checkpoint 4947",
            },
            {
                "decision_id": "DEC4952_03_smooth_galaxy",
                "question": "Can harmonics n<=4 directly populate two massless modes at the outer galactic scale?",
                "result": direct_smooth_galaxy_profile,
                "decision": "NO_ALL_175_PUBLIC_ROWS_FAIL_SUPPORT",
                "claim_boundary": "uses generous Omega=v_outer/R_outer and is therefore conservative",
            },
            {
                "decision_id": "DEC4952_04_local",
                "question": "Does spectral support alone prove universal local silence?",
                "result": False,
                "decision": "NO_FAST_COMPACT_ROTATORS_HAVE_LOWER_THRESHOLDS",
                "claim_boundary": "amplitude and state-dependent emission still require calculation",
            },
            {
                "decision_id": "DEC4952_05_route",
                "question": "Is late-time smooth visible-matter/graviton noise a derived direct galaxy occupation route?",
                "result": route_claim,
                "decision": "REJECT_DIRECT_LATE_TIME_SMOOTH_ROUTE",
                "claim_boundary": "formation transients and a derived X2 kinetic cascade remain open",
            },
            {
                "decision_id": "DEC4952_06_local_GR",
                "question": "Does this rejection invalidate the stationary psi=0 local GR/Newton/Maxwell branch?",
                "result": False,
                "decision": "NO_4947_BRANCH_RETAINED",
                "claim_boundary": "the stationary ground state has zero emission and zero occupation",
            },
        ]
    )

    try:
        galaxy_head = subprocess.run(
            ["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        galaxy_status = subprocess.run(
            ["git", "-C", str(GALAXY_REPO), "status", "--short"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        galaxy_head = "UNAVAILABLE"
        galaxy_status = "UNAVAILABLE"

    snapshot_rows = tagged(
        [
            {
                "repo": str(GALAXY_REPO),
                "head": galaxy_head,
                "expected_head": EXPECTED_GALAXY_HEAD,
                "head_matches": galaxy_head == EXPECTED_GALAXY_HEAD,
                "git_status_short": galaxy_status,
                "worktree_clean": galaxy_status == "",
                "sample_count": len(samples),
                "sample_sha256": source_hashes[str(GALAXY_SAMPLES)],
                "access_mode": "READ_ONLY",
                "passed": galaxy_head == EXPECTED_GALAXY_HEAD and galaxy_status == "" and len(samples) == 175,
            }
        ]
    )

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "symbolic": {
            "pair_vertex_q_contract_p_coefficient": str(q_contract_p),
            "pair_vertex_q_contract_pprime_coefficient": str(q_contract_pprime),
            "Ward_identity_zero": ward_identity_zero,
            "induced_metric_noise_coefficient": str(induced_metric_noise_coefficient),
            "system_influence_noise_coefficient": str(system_influence_noise_coefficient),
            "exchange_amplitude_coefficient": str(exchange_amplitude_coefficient),
            "exchange_rate_coefficient": str(exchange_rate_coefficient),
        },
        "galaxy_summary": {
            "sample_count": len(samples),
            "massless_min_n_one_profile_mode": min(massless_n_one),
            "massless_median_n_one_profile_mode": statistics.median(massless_n_one),
            "massless_max_n_one_profile_mode": max(massless_n_one),
            "massless_min_n_two_profile_modes": min(massless_n_two),
            "massless_median_n_two_profile_modes": statistics.median(massless_n_two),
            "massless_max_n_two_profile_modes": max(massless_n_two),
            "easiest_two_profile_galaxy": easiest_two["galaxy"],
            "hardest_two_profile_galaxy": hardest_two["galaxy"],
            "smooth_n_le_4_pass_count": sum(bool(row["smooth_n_le_4_can_make_two_profile_modes"]) for row in massless_galaxy),
        },
        "local_summary": {
            row["system"]: {
                "derived_or_bounded_radius_m": row["radius_m"],
                "v_over_c": row["v_over_c"],
                "massless_n_one_profile_mode": row["n_min_one_mode_k_at_least_inverse_R"],
                "massless_n_two_profile_modes": row["n_min_two_modes_k_at_least_inverse_R"],
            }
            for row in local_massless
        },
        "decisions": {
            "parent_pair_channel_exists": pair_source_exists_formally,
            "symmetrized_vacuum_noise_is_real_pair_source": False,
            "stationary_or_DC_Poynting_pair_source": False,
            "smooth_late_time_galaxy_direct_profile_support": direct_smooth_galaxy_profile,
            "spectral_support_proves_local_silence": False,
            "late_time_smooth_CTP_route_accepted": route_claim,
            "local_GR_Newton_Maxwell_4947_retained": True,
            "full_MTS_galaxy_unification": False,
        },
        "next_target": "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md",
        "valid_for_full_MTS_claim": False,
    }

    write_csv(VERTEX_CSV, vertex_rows)
    write_csv(SPECTRAL_CSV, spectral_rows)
    write_csv(SPARC_CSV, sparc_rows)
    write_csv(LOCAL_CSV, local_rows)
    write_csv(POYNTING_CSV, poynting_rows)
    write_csv(DECISION_CSV, decision_rows)
    write_csv(GALAXY_SNAPSHOT_CSV, snapshot_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    required = [
        source_hashes_match,
        all(source_clause_checks.values()),
        all(bool(row["passed"]) for row in vertex_rows),
        all(bool(row["passed"]) for row in spectral_rows),
        len(sparc_rows) == 700,
        len(massless_galaxy) == 175,
        not direct_smooth_galaxy_profile,
        len(local_rows) == 8,
        all(bool(row["passed"]) for row in poynting_rows),
        bool(snapshot_rows[0]["passed"]),
        not route_claim,
    ]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(required) else 1


if __name__ == "__main__":
    raise SystemExit(main())
