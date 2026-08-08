from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
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
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4953_VALIDATION.csv"

RESULT_JSON = SOURCE / "formation_X2_cascade_and_injection_results.json"
KERNEL_CSV = SOURCE / "X2_scattering_kernel.csv"
INVARIANT_CSV = SOURCE / "X2_collision_invariant_gate.csv"
SPECTRAL_CSV = SOURCE / "formation_spectral_number_bound.csv"
SPARC_INJECTION_CSV = SOURCE / "SPARC_formation_injection_gate.csv"
SPARC_NONLINEAR_CSV = SOURCE / "SPARC_X2_nonlinearity_gate.csv"
LOCAL_CSV = SOURCE / "local_compact_X2_injection_gate.csv"
NUMBER_CHANGE_CSV = SOURCE / "X2_number_change_scaling.csv"
DECISION_CSV = SOURCE / "formation_X2_composite_route_decision.csv"

RESEARCH_SCRIPT = POST / "scripts" / "Y5_R2FR_4953_formation_X2_cascade_and_injection_gate.py"
CHECKPOINT = POST / "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "969-PPC4161-formation-X2-cascade-and-local-injection-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

OCCUPATION_CSV = POST / "source-intake" / "functional_rg" / "4949" / "SPARC_outer_occupation_scale_diagnostic.csv"
HARMONIC_CSV = POST / "source-intake" / "functional_rg" / "4952" / "SPARC_outer_harmonic_support_gate.csv"
LOCAL_SUPPORT_CSV = POST / "source-intake" / "functional_rg" / "4952" / "local_compact_rotator_harmonic_support_gate.csv"
PLANCK_PDF = SOURCE / "1807.06209v4.pdf"

MARKER = "MTS_4953_FORMATION_X2_CASCADE_AND_INJECTION_GATE"
VALIDATION_MARKER = "MTS_4953_INDEPENDENT_VALIDATION"
LIGHT_SPEED = 299_792_458.0
HBAR_EV_S = 6.582_119_569e-16
HBARC_EV_M = 1.973_269_804e-7
JOULE_PER_EV = 1.602_176_634e-19
SOLAR_MASS = 1.988_47e30
YEAR_S = 365.25 * 24.0 * 3600.0
FORMATION_TIME_S = 10.0e9 * YEAR_S
A_MAX = 1090.92
DECIMAL_PI = Decimal("3.1415926535897932384626433832795028841971693993751")
DECIMAL_C = Decimal(1) / Decimal("2.435e27") ** 4
DECIMAL_HBARC = Decimal("1.973269804e-7")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def close(left: float, right: float, relative: float = 2.0e-12, absolute: float = 0.0) -> bool:
    return math.isclose(left, right, rel_tol=relative, abs_tol=absolute)


def rho_ev4(value_j_m3: float) -> float:
    return value_j_m3 * HBARC_EV_M**3 / JOULE_PER_EV


def add(
    rows: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    outputs = [
        RESULT_JSON,
        KERNEL_CSV,
        INVARIANT_CSV,
        SPECTRAL_CSV,
        SPARC_INJECTION_CSV,
        SPARC_NONLINEAR_CSV,
        LOCAL_CSV,
        NUMBER_CHANGE_CSV,
        DECISION_CSV,
    ]
    required_paths = outputs + [
        RESEARCH_SCRIPT,
        CHECKPOINT,
        PROVENANCE,
        FORMAL,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
        OCCUPATION_CSV,
        HARMONIC_CSV,
        LOCAL_SUPPORT_CSV,
        PLANCK_PDF,
    ]
    missing = [str(path) for path in required_paths if not path.is_file()]
    add(checks, "VAL4953_00_paths", "all source, script, document and output paths exist", [], missing, not missing)
    if missing:
        VALIDATION.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
            writer.writeheader()
            writer.writerows(checks)
        return 1

    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    kernel = read_csv(KERNEL_CSV)
    invariants = read_csv(INVARIANT_CSV)
    spectral = read_csv(SPECTRAL_CSV)
    injection = read_csv(SPARC_INJECTION_CSV)
    nonlinear = read_csv(SPARC_NONLINEAR_CSV)
    local = read_csv(LOCAL_CSV)
    number_change = read_csv(NUMBER_CHANGE_CSV)
    decisions = read_csv(DECISION_CSV)
    tables = (kernel, invariants, spectral, injection, nonlinear, local, number_change, decisions)

    marker_ok = result["checkpoint_marker"] == MARKER and all(
        row["checkpoint_marker"] == MARKER for table in tables for row in table
    )
    add(checks, "VAL4953_01_marker", "result and every row use the 4953 marker", MARKER, result["checkpoint_marker"], marker_ok)
    nonclaim_ok = all(not as_bool(row["valid_for_full_MTS_claim"]) for table in tables for row in table)
    add(checks, "VAL4953_02_nonclaim", "every generated evidence row remains nonclaim", True, nonclaim_ok, nonclaim_ok)

    source_hashes_ok = result["source_hashes_match"] and all(
        Path(path).is_file() and digest(Path(path)) == value for path, value in result["source_hashes"].items()
    )
    add(checks, "VAL4953_03_hashes", "all locked source hashes independently recompute", True, source_hashes_ok, source_hashes_ok)
    clauses_ok = all(result["source_clause_checks"].values())
    add(checks, "VAL4953_04_source_clauses", "all parent and primary-source clauses were located", True, result["source_clause_checks"], clauses_ok)
    add(
        checks,
        "VAL4953_05_planck_source",
        "Planck source hash and conservative stretch are locked",
        "8e172730...;1090.92",
        f"{digest(PLANCK_PDF)[:12]};{result['constants']['max_post_recombination_stretch']}",
        digest(PLANCK_PDF) == "8e172730faf07c9f4ff3fdcc7043f76ed67df6f76066d47df30d693025b6ce77"
        and result["constants"]["Planck_z_star"] == 1089.92
        and result["constants"]["max_post_recombination_stretch"] == A_MAX,
    )

    cosine, mandelstam_s, coefficient = sp.symbols("x s c", real=True)
    amplitude = coefficient * mandelstam_s**2 * (3 + cosine**2) / 4
    sigma = sp.simplify(sp.integrate(amplitude**2, (cosine, -1, 1)) / (64 * sp.pi * mandelstam_s))
    a0 = sp.simplify(sp.integrate(amplitude, (cosine, -1, 1)) / (32 * sp.pi))
    amplitude_ok = str(result["symbolic"]["cm_amplitude"]).replace("c_ess", "c") == str(amplitude)
    sigma_ok = sigma == 7 * coefficient**2 * mandelstam_s**3 / (320 * sp.pi)
    a0_ok = a0 == 5 * coefficient * mandelstam_s**2 / (96 * sp.pi)
    add(checks, "VAL4953_06_amplitude", "CM X2 amplitude independently reconstructs", str(amplitude), result["symbolic"]["cm_amplitude"], amplitude_ok)
    add(checks, "VAL4953_07_sigma", "identical-final cross section independently integrates", "7c2s3/(320pi)", sigma, sigma_ok)
    add(checks, "VAL4953_08_a0", "s-wave independently integrates", "5cs2/(96pi)", a0, a0_ok)

    p1, p2, p3 = sp.symbols("p1 p2 p3")
    p4 = p1 + p2 - p3
    number_zero = 1 + 1 - 1 - 1 == 0
    momentum_zero = sp.simplify(p3 + p4 - p1 - p2) == 0
    add(checks, "VAL4953_09_number_invariant", "Delta W vanishes for W=1", 0, 1 + 1 - 1 - 1, number_zero)
    add(checks, "VAL4953_10_momentum_invariant", "Delta W vanishes for W=pnu", 0, sp.simplify(p3 + p4 - p1 - p2), momentum_zero)
    kernel_ok = len(kernel) == 6 and all(as_bool(row["passed"]) for row in kernel)
    invariant_ok = len(invariants) == 9 and all(as_bool(row["passed"]) for row in invariants)
    add(checks, "VAL4953_11_kernel_rows", "all six exact scattering rows pass", "6 pass", f"{len(kernel)} rows", kernel_ok)
    add(checks, "VAL4953_12_invariant_rows", "all nine kinetic classification rows pass", "9 pass", f"{len(invariants)} rows", invariant_ok)

    occupation = read_csv(OCCUPATION_CSV)
    harmonic = [row for row in read_csv(HARMONIC_CSV) if row["compton_case"] == "massless"]
    positive_count = sum(row["positive_outer_residual"] == "True" for row in occupation)
    add(checks, "VAL4953_13_public_input", "public occupation and harmonic inputs have 175 matched rows", "175;175", f"{len(occupation)};{len(harmonic)}", len(occupation) == 175 and len(harmonic) == 175)
    add(checks, "VAL4953_14_positive_targets", "positive outer-residual count is explicit", 173, positive_count, positive_count == 173)
    add(checks, "VAL4953_15_injection_shape", "six injection cases exist for every public row", 1050, len(injection), len(injection) == 1050)

    formula_failures = 0
    for row in injection:
        radius_m = float(row["outer_radius_m"])
        profile_energy = HBARC_EV_M / radius_m
        injection_energy = float(row["injection_quantum_energy_eV"])
        stretch = injection_energy / profile_energy
        fixed_fraction = min(1.0, 1.0 / stretch)
        redshift_fraction = min(1.0, A_MAX / stretch)
        if not (
            close(float(row["profile_quantum_energy_eV"]), profile_energy)
            and close(float(row["multiplicity_ratio_injection_to_profile"]), stretch)
            and close(float(row["fixed_final_energy_number_fraction_max"]), fixed_fraction)
            and close(float(row["redshift_assisted_number_fraction_max"]), redshift_fraction)
            and as_bool(row["two_to_two_changes_particle_number"]) is False
        ):
            formula_failures += 1
    add(checks, "VAL4953_16_injection_formulas", "all number and redshift ceilings independently recompute", 0, formula_failures, formula_failures == 0)

    positive_injection = [row for row in injection if as_bool(row["positive_outer_residual_target"])]
    high_cases = {
        "white_dwarf_fundamental_pair_quantum",
        "neutron_star_fundamental_pair_quantum",
        "one_GeV_quantum",
        "UHE_1e20_eV_quantum",
    }
    high = [row for row in positive_injection if row["injection_case"] in high_cases]
    high_fail = sum(float(row["redshift_assisted_number_fraction_max"]) < 1.0 for row in high)
    direct = [row for row in positive_injection if row["injection_case"] == "direct_profile_quantum"]
    supported = [row for row in positive_injection if row["injection_case"] == "minimum_4952_supported_profile_pair"]
    add(checks, "VAL4953_17_high_frequency", "all positive high-frequency rows fail maximal redshift", "692/692", f"{high_fail}/{len(high)}", len(high) == 692 and high_fail == 692)
    add(checks, "VAL4953_18_direct_profile", "all direct profile rows pass number accounting only", 173, sum(float(row["fixed_final_energy_number_fraction_max"]) == 1.0 for row in direct), len(direct) == 173 and all("AMPLITUDE_UNSOLVED" in row["route_status"] for row in direct))
    supported_ratios = [float(row["multiplicity_ratio_injection_to_profile"]) for row in supported]
    supported_ok = len(supported) == 173 and min(supported_ratios) >= 1.0 and max(supported_ratios) < 1.001
    add(checks, "VAL4953_19_supported_harmonic", "4952 minimum supported pair is profile-energy scale but amplitude-unsolved", "1<=ratio<1.001", f"{min(supported_ratios)}..{max(supported_ratios)}", supported_ok)

    nonlinear_failures = 0
    positive_phase_scales: list[float] = []
    for row in nonlinear:
        density_j = float(row["required_effective_energy_density_J_m3"])
        density_ev4 = rho_ev4(density_j)
        radius_m = float(row["outer_radius_m"])
        phase_scale = density_ev4 * LIGHT_SPEED / radius_m * FORMATION_TIME_S
        if as_bool(row["positive_outer_residual_target"]):
            positive_phase_scales.append(phase_scale)
        if not (
            close(float(row["required_effective_energy_density_eV4"]), density_ev4)
            and close(float(row["phase_scale_per_c_ess_eV4"]), phase_scale, absolute=1.0e-300)
            and not as_bool(row["two_to_two_can_build_required_number"])
        ):
            nonlinear_failures += 1
    add(checks, "VAL4953_20_nonlinear_rows", "all 175 phase-scale rows independently recompute", 0, nonlinear_failures, len(nonlinear) == 175 and nonlinear_failures == 0)
    natural_phase_max = max(float(row["natural_secular_phase_upper_comparator"]) for row in nonlinear)
    add(checks, "VAL4953_21_natural_galaxy", "natural galaxy phase maximum matches result and is tiny", result["execution"]["natural_galaxy_phase_max"], natural_phase_max, close(natural_phase_max, result["execution"]["natural_galaxy_phase_max"]) and natural_phase_max < 1.0e-100)

    source_local = {row["system"]: row for row in read_csv(LOCAL_SUPPORT_CSV) if row["compton_case"] == "massless"}
    masses = {
        "J2211+1136_white_dwarf": 1.268 * SOLAR_MASS,
        "PSR_J1748-2446ad_neutron_star": 2.0 * SOLAR_MASS,
    }
    local_failures = 0
    for row in local:
        system = row["system"]
        radius = float(source_local[system]["radius_m"])
        omega = float(source_local[system]["omega_rad_s"])
        rotational_energy = 0.2 * masses[system] * radius**2 * omega**2
        density_j = rotational_energy / (4.0 * math.pi * radius**3 / 3.0)
        density_ev4 = rho_ev4(density_j)
        phase_scale = density_ev4 * omega / 2.0 * FORMATION_TIME_S
        ceilings = [value / phase_scale for value in positive_phase_scales]
        if not (
            close(float(row["rotational_energy_density_J_m3"]), density_j)
            and close(float(row["rotational_energy_density_eV4"]), density_ev4)
            and close(float(row["galaxy_to_local_injection_efficiency_ceiling_median"]), statistics.median(ceilings))
            and not as_bool(row["equal_injection_efficiency_has_universal_phase_window"])
        ):
            local_failures += 1
    add(checks, "VAL4953_22_local_rows", "both maximal compact comparators independently recompute with no equal-efficiency window", 0, local_failures, len(local) == 2 and local_failures == 0)
    compact_phase_max = max(float(row["natural_secular_phase_upper_comparator"]) for row in local)
    add(checks, "VAL4953_23_natural_compact", "natural compact phase maximum matches result and is tiny", result["execution"]["natural_compact_phase_max"], compact_phase_max, close(compact_phase_max, result["execution"]["natural_compact_phase_max"]) and compact_phase_max < 1.0e-50)

    decimal_failures = 0
    for row in number_change:
        energy = Decimal(row["energy_eV"])
        coupling = DECIMAL_C * energy**4
        sigma_m2 = Decimal(7) * DECIMAL_C**2 * energy**6 * DECIMAL_HBARC**2 / (Decimal(5) * DECIMAL_PI)
        ratio = coupling**2
        if not (
            Decimal(row["dimensionless_g_X2_abs_cE4"]) == coupling.quantize(Decimal(row["dimensionless_g_X2_abs_cE4"]))
            and Decimal(row["sigma_22_natural_m2"]) == sigma_m2.quantize(Decimal(row["sigma_22_natural_m2"]))
            and Decimal(row["sigma_24_over_sigma_22_parametric_upper_without_phase_space"]) == ratio.quantize(Decimal(row["sigma_24_over_sigma_22_parametric_upper_without_phase_space"]))
            and Decimal(row["sigma_22_natural_m2"]) > 0
            and Decimal(row["sigma_24_over_sigma_22_parametric_upper_without_phase_space"]) > 0
        ):
            decimal_failures += 1
    add(checks, "VAL4953_24_number_change", "all five high-precision natural scaling rows recompute without underflow", 0, decimal_failures, len(number_change) == 5 and decimal_failures == 0)
    uhe = next(row for row in number_change if row["energy_case"] == "UHE_1e20_eV")
    uhe_ok = close(float(uhe["dimensionless_g_X2_abs_cE4"]), 2.8444882085516576e-30) and close(float(uhe["sigma_22_natural_m2"]), 1.4039750138734436e-113) and close(float(uhe["sigma_24_over_sigma_22_parametric_upper_without_phase_space"]), 8.091113168589416e-60)
    add(checks, "VAL4953_25_UHE", "UHE natural comparator reproduces declared values", True, uhe_ok, uhe_ok)

    decision_statuses = {row["status"] for row in decisions}
    decision_ok = len(decisions) == 9 and {
        "ROUTE_REJECTED_EXACTLY",
        "EXECUTED_ROUTE_REJECTED",
        "OPEN_SOURCE_SPECTRUM_NOT_A_CASCADE",
        "FULL_2PI_NUMBER_CHANGE_KERNEL_REQUIRED",
        "4947_LOCAL_BRANCH_RETAINED",
        "FULL_MTS_PROMOTION_BLOCKED",
    }.issubset(decision_statuses)
    add(checks, "VAL4953_26_decisions", "route decision distinguishes exact rejection from open off-shell work", True, sorted(decision_statuses), decision_ok)

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8-sig")
    formal_text = FORMAL.read_text(encoding="utf-8-sig")
    provenance_text = PROVENANCE.read_text(encoding="utf-8-sig")
    docs_ok = all(
        token in checkpoint_text + formal_text + provenance_text
        for token in (
            "MTS_FORMATION_X2_CASCADE_LOCAL_INJECTION_DECISION_4953",
            "PPC4161_FORMATION_X2_CASCADE_LOCAL_INJECTION_4953",
            "MTS_FORMATION_X2_CASCADE_PROVENANCE_4953",
            "full MTS galaxy unification                     = false",
        )
    )
    add(checks, "VAL4953_27_documents", "checkpoint, formal decision and provenance carry required markers and nonclaim boundary", True, docs_ok, docs_ok)

    claims = read_csv(CLAIMS)
    claim_rows = [row for row in claims if row["claim_id"] == "L-795"]
    claim_ok = len(claim_rows) == 1 and "off-shell" in claim_rows[0]["key_risk"] and "FULL_MTS_FALSE" in claim_rows[0]["notes"]
    add(checks, "VAL4953_28_claim", "claim L-795 is unique and preserves off-shell/full-MTS boundary", True, len(claim_rows), claim_ok)
    variables = read_csv(VARIABLES)
    required_symbols = {
        "X2ScatteringKernel4953_MTS",
        "X2CollisionInvariant4953_MTS",
        "FormationSpectralNumberBound4953_MTS",
        "MaxPostRecombinationStretch4953_MTS",
        "GalaxyFormationInjectionGate4953_MTS",
        "NaturalX2Comparator4953_MTS",
        "LocalInjectionEfficiencyCeiling4953_MTS",
        "X2NumberChangeScaling4953_MTS",
        "PredictivityStatus4953_MTS",
    }
    present_symbols = {row["symbol"] for row in variables}
    add(checks, "VAL4953_29_variables", "all nine canonical 4953 variables are registered", sorted(required_symbols), sorted(required_symbols & present_symbols), required_symbols.issubset(present_symbols))
    equation_ok = "## 1.246 Formation `X2` collision invariants and spectral-number bound" in EQUATIONS.read_text(encoding="utf-8-sig")
    red_ok = "## 197. Scattering is not particle multiplication" in RED_TEAM.read_text(encoding="utf-8-sig")
    spine_ok = "PPC4161_FORMATION_X2_CASCADE_LOCAL_INJECTION_4953" in SPINE.read_text(encoding="utf-8-sig")
    resume_ok = "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel" in RESUME.read_text(encoding="utf-8-sig")
    add(checks, "VAL4953_30_equation", "equation register contains 1.246", True, equation_ok, equation_ok)
    add(checks, "VAL4953_31_red_team", "red-team register contains item 197", True, red_ok, red_ok)
    add(checks, "VAL4953_32_spine", "unification spine contains the 4953 decision", True, spine_ok, spine_ok)
    add(checks, "VAL4953_33_resume", "resume advances to the finite-time number-changing target", True, resume_ok, resume_ok)

    before_hashes = {path: digest(path) for path in outputs}
    rerun = subprocess.run([sys.executable, str(RESEARCH_SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False)
    after_hashes = {path: digest(path) for path in outputs}
    deterministic_ok = rerun.returncode == 0 and before_hashes == after_hashes
    add(checks, "VAL4953_34_determinism", "research script reruns successfully with byte-identical outputs", "return 0 and identical", f"return {rerun.returncode}; identical={before_hashes == after_hashes}", deterministic_ok)
    result_hash_ok = json.loads(RESULT_JSON.read_text(encoding="utf-8"))["decision"]["full_MTS"] is False
    add(checks, "VAL4953_35_final_nonclaim", "deterministic rerun still records full_MTS=false", False, not result_hash_ok, result_hash_ok)

    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    return 0 if all(as_bool(row["passed"]) for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
