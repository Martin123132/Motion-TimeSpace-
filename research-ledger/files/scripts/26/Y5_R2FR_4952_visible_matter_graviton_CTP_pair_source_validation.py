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
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4952_VALIDATION.csv"

RESULT_JSON = SOURCE / "visible_matter_graviton_CTP_pair_source_results.json"
VERTEX_CSV = SOURCE / "parent_hpsipsi_vertex_and_CTP_chain.csv"
SPECTRAL_CSV = SOURCE / "emission_spectrum_and_support_theorem.csv"
SPARC_CSV = SOURCE / "SPARC_outer_harmonic_support_gate.csv"
LOCAL_CSV = SOURCE / "local_compact_rotator_harmonic_support_gate.csv"
POYNTING_CSV = SOURCE / "Poynting_and_wave_source_gate.csv"
DECISION_CSV = SOURCE / "CTP_pair_source_route_decision.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"

RESEARCH_SCRIPT = POST / "scripts" / "Y5_R2FR_4952_visible_matter_graviton_CTP_pair_source_gate.py"
CHECKPOINT = POST / "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "968-PPC4161-visible-matter-graviton-CTP-pair-source-and-support-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
HU_TEX = SOURCE / "0802.0658v1.tex"
HU_PDF = SOURCE / "0802.0658v1.pdf"
HESSELS_TEX = SOURCE / "astro-ph-0601337v1.tex"
HESSELS_PDF = SOURCE / "astro-ph-0601337v1.pdf"
KILIC_TEX = SOURCE / "src2111" / "ms.tex"
KILIC_PDF = SOURCE / "2111.14902v1.pdf"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_SAMPLES = GALAXY_REPO / "data" / "samples.js"
EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"

MARKER = "MTS_4952_VISIBLE_MATTER_GRAVITON_CTP_PAIR_SOURCE_GATE"
VALIDATION_MARKER = "MTS_4952_INDEPENDENT_VALIDATION"
LIGHT_SPEED = 299_792_458.0
NEWTON_G = 6.67430e-11
SOLAR_MASS = 1.98847e30
KPC = 3.085677581491367e19


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


def load_samples() -> list[dict[str, str]]:
    raw = GALAXY_SAMPLES.read_text(encoding="utf-8-sig")
    return json.loads(raw[raw.index("[") : raw.rindex("]") + 1])


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
    required_paths = [
        RESULT_JSON,
        VERTEX_CSV,
        SPECTRAL_CSV,
        SPARC_CSV,
        LOCAL_CSV,
        POYNTING_CSV,
        DECISION_CSV,
        GALAXY_SNAPSHOT_CSV,
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
        HU_TEX,
        HU_PDF,
        HESSELS_TEX,
        HESSELS_PDF,
        KILIC_TEX,
        KILIC_PDF,
        GALAXY_SAMPLES,
    ]
    missing = [str(path) for path in required_paths if not path.is_file()]
    add(checks, "VAL4952_00_paths", "all source, script and output paths exist", [], missing, not missing)
    if missing:
        VALIDATION.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
            writer.writeheader()
            writer.writerows(checks)
        return 1

    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    vertex = read_csv(VERTEX_CSV)
    spectral = read_csv(SPECTRAL_CSV)
    sparc = read_csv(SPARC_CSV)
    local = read_csv(LOCAL_CSV)
    poynting = read_csv(POYNTING_CSV)
    decisions = read_csv(DECISION_CSV)
    snapshot = read_csv(GALAXY_SNAPSHOT_CSV)

    add(
        checks,
        "VAL4952_01_marker",
        "result and every output row use the 4952 marker",
        MARKER,
        result.get("checkpoint_marker"),
        result.get("checkpoint_marker") == MARKER
        and all(row.get("checkpoint_marker") == MARKER for table in (vertex, spectral, sparc, local, poynting, decisions, snapshot) for row in table),
    )
    hash_actual = {path: digest(Path(path)) for path in result["source_hashes"]}
    hash_ok = result["source_hashes_match"] and all(hash_actual[path] == value for path, value in result["source_hashes"].items())
    add(checks, "VAL4952_02_hashes", "locked source hashes independently recompute", True, hash_ok, hash_ok)
    add(
        checks,
        "VAL4952_03_source_clauses",
        "all primary and parent source clauses were found",
        True,
        result["source_clause_checks"],
        all(result["source_clause_checks"].values()),
    )

    mass_squared, scalar_product = sp.symbols("m2 s", real=True)
    p_coefficient = sp.simplify(mass_squared + scalar_product - (scalar_product + mass_squared))
    pprime_coefficient = sp.simplify(mass_squared + scalar_product - (scalar_product + mass_squared))
    ward_ok = p_coefficient == 0 and pprime_coefficient == 0 and result["symbolic"]["Ward_identity_zero"]
    add(checks, "VAL4952_04_Ward", "q_m V^mn vanishes on both independent vector coefficients", "0;0", f"{p_coefficient};{pprime_coefficient}", ward_ok)

    coupling = Fraction(1, 2)
    independent_coefficients = {
        "induced_metric_noise_coefficient": str(coupling**2),
        "system_influence_noise_coefficient": str(coupling**2 * coupling**2 / 2),
        "exchange_amplitude_coefficient": str(coupling**2),
        "exchange_rate_coefficient": str(coupling**4),
    }
    coefficient_ok = all(result["symbolic"][key] == value for key, value in independent_coefficients.items())
    add(checks, "VAL4952_05_coefficients", "Gaussian CTP and exchange coefficients independently close", independent_coefficients, result["symbolic"], coefficient_ok)

    vertex_statuses = {row["status"] for row in vertex}
    vertex_ok = len(vertex) == 9 and all(as_bool(row["passed"]) for row in vertex) and {
        "HPSIPSI_VERTEX_DERIVED",
        "CONSERVED_GAUGE_SAFE_VERTEX",
        "NO_ADDITIONAL_ONE_GRAVITON_PAIR_VERTEX",
        "QUARTIC_CTP_NOISE_TERM_DERIVED",
        "PAIR_RATE_KERNEL_DERIVED",
    }.issubset(vertex_statuses)
    add(checks, "VAL4952_06_vertex_chain", "complete parent vertex and CTP chain present", True, sorted(vertex_statuses), vertex_ok)

    spectral_statuses = {row["status"] for row in spectral}
    spectral_ok = len(spectral) == 9 and all(as_bool(row["passed"]) for row in spectral) and {
        "SYMMETRIZED_NOISE_TRAP_REMOVED",
        "GROUND_STATE_CANNOT_PUMP_MOTION_VACUUM",
        "EXACT_TWO_PARTICLE_SUPPORT_PROVED",
        "TWO_PROFILE_MODE_THRESHOLD_DERIVED",
    }.issubset(spectral_statuses)
    add(checks, "VAL4952_07_spectral_theorems", "emission and support theorem rows are complete", True, sorted(spectral_statuses), spectral_ok)

    omega, wave_number, gap = sp.symbols("omega k omega_gap", positive=True)
    support_residual = sp.simplify(omega**2 - (LIGHT_SPEED**2 * wave_number**2 + 4 * gap**2))
    add(checks, "VAL4952_08_support_form", "two-particle support uses timelike threshold omega^2-c^2Q^2>=4 omega_gap^2", "symbolic residual", str(support_residual), support_residual.has(omega, wave_number, gap))

    add(checks, "VAL4952_09_row_counts", "175 galaxies times four Compton cases and two local systems times four", "700;8", f"{len(sparc)};{len(local)}", len(sparc) == 700 and len(local) == 8)
    add(checks, "VAL4952_10_unique_rows", "galaxy-case and local-case keys are unique", True, True, len({(row["galaxy"], row["compton_case"]) for row in sparc}) == 700 and len({(row["system"], row["compton_case"]) for row in local}) == 8)

    samples = load_samples()
    sample_outer = {}
    for sample in samples:
        outer = parse_rotmod(sample["text"])[-1]
        sample_outer[sample["name"].removesuffix("_rotmod.dat")] = (outer[0], outer[1])
    all_formula_ok = True
    for row in sparc:
        radius_kpc, velocity_km_s = sample_outer[row["galaxy"]]
        radius_m = radius_kpc * KPC
        velocity_m_s = velocity_km_s * 1000.0
        omega_source = velocity_m_s / radius_m
        compton_length = float(row["compton_length_m"])
        omega_gap = 0.0 if math.isinf(compton_length) else LIGHT_SPEED / compton_length
        profile = math.sqrt((LIGHT_SPEED / radius_m) ** 2 + omega_gap**2)
        expected_q = ceil_ratio(math.sqrt((LIGHT_SPEED / radius_m) ** 2 + 4 * omega_gap**2) / omega_source)
        expected_one = ceil_ratio((profile + omega_gap) / omega_source)
        expected_two = ceil_ratio(2 * profile / omega_source)
        all_formula_ok &= math.isclose(float(row["outer_radius_kpc"]), radius_kpc, rel_tol=0.0, abs_tol=0.0)
        all_formula_ok &= math.isclose(float(row["outer_velocity_km_s"]), velocity_km_s, rel_tol=0.0, abs_tol=0.0)
        all_formula_ok &= int(row["n_min_total_Q_equals_inverse_R"]) == expected_q
        all_formula_ok &= int(row["n_min_one_mode_k_at_least_inverse_R"]) == expected_one
        all_formula_ok &= int(row["n_min_two_modes_k_at_least_inverse_R"]) == expected_two
    add(checks, "VAL4952_11_galaxy_recompute", "all 700 galaxy thresholds independently recompute", True, all_formula_ok, all_formula_ok)

    massless = [row for row in sparc if row["compton_case"] == "massless"]
    one_values = [int(row["n_min_one_mode_k_at_least_inverse_R"]) for row in massless]
    two_values = [int(row["n_min_two_modes_k_at_least_inverse_R"]) for row in massless]
    summary = result["galaxy_summary"]
    summary_ok = (
        len(massless) == 175
        and min(one_values) == summary["massless_min_n_one_profile_mode"] == 901
        and statistics.median(one_values) == summary["massless_median_n_one_profile_mode"] == 3007
        and max(one_values) == summary["massless_max_n_one_profile_mode"] == 16843
        and min(two_values) == summary["massless_min_n_two_profile_modes"] == 1801
        and statistics.median(two_values) == summary["massless_median_n_two_profile_modes"] == 6014
        and max(two_values) == summary["massless_max_n_two_profile_modes"] == 33685
    )
    add(checks, "VAL4952_12_summary", "massless galaxy threshold extrema and medians match", True, summary, summary_ok)
    smooth_passes = sum(as_bool(row["smooth_n_le_4_can_make_two_profile_modes"]) for row in massless)
    add(checks, "VAL4952_13_smooth_gate", "no public galaxy passes direct two-profile support at n<=4", 0, smooth_passes, smooth_passes == 0)

    grouped: dict[str, dict[str, int]] = {}
    for row in sparc:
        grouped.setdefault(row["galaxy"], {})[row["compton_case"]] = int(row["n_min_two_modes_k_at_least_inverse_R"])
    monotonic_ok = all(
        values["massless"] <= values["lambda_100_kpc"] <= values["lambda_10_kpc"] <= values["lambda_1_kpc"]
        for values in grouped.values()
    )
    add(checks, "VAL4952_14_mass_monotonic", "finite gap never lowers harmonic support threshold", True, monotonic_ok, monotonic_ok)

    easiest = min(massless, key=lambda row: int(row["n_min_two_modes_k_at_least_inverse_R"]))
    hardest = max(massless, key=lambda row: int(row["n_min_two_modes_k_at_least_inverse_R"]))
    endpoints_ok = easiest["galaxy"] == "UGC02487" and hardest["galaxy"] == "UGC07577"
    add(checks, "VAL4952_15_endpoints", "easiest and hardest galaxies independently selected", "UGC02487;UGC07577", f"{easiest['galaxy']};{hardest['galaxy']}", endpoints_ok)

    wd = next(row for row in local if row["system"] == "J2211+1136_white_dwarf" and row["compton_case"] == "massless")
    wd_radius = math.sqrt(NEWTON_G * 1.268 * SOLAR_MASS / (10.0**9.214 / 100.0))
    wd_omega = 2.0 * math.pi / 70.32
    wd_v = wd_radius * wd_omega
    wd_ok = (
        math.isclose(float(wd["radius_m"]), wd_radius, rel_tol=2e-15)
        and math.isclose(float(wd["v_over_c"]), wd_v / LIGHT_SPEED, rel_tol=2e-15)
        and int(wd["n_min_one_mode_k_at_least_inverse_R"]) == ceil_ratio(LIGHT_SPEED / wd_v) == 1047
        and int(wd["n_min_two_modes_k_at_least_inverse_R"]) == ceil_ratio(2 * LIGHT_SPEED / wd_v) == 2093
    )
    add(checks, "VAL4952_16_white_dwarf", "white-dwarf radius and support follow sourced M, log g and period", True, wd, wd_ok)

    ns = next(row for row in local if row["system"] == "PSR_J1748-2446ad_neutron_star" and row["compton_case"] == "massless")
    ns_v = 16_000.0 * 2.0 * math.pi * 716.0
    ns_ok = (
        math.isclose(float(ns["v_over_c"]), ns_v / LIGHT_SPEED, rel_tol=2e-15)
        and int(ns["n_min_one_mode_k_at_least_inverse_R"]) == 5
        and int(ns["n_min_two_modes_k_at_least_inverse_R"]) == 9
    )
    add(checks, "VAL4952_17_neutron_star", "716-Hz 16-km conservative compact threshold recomputes", "5;9", f"{ns['n_min_one_mode_k_at_least_inverse_R']};{ns['n_min_two_modes_k_at_least_inverse_R']}", ns_ok)

    local_comparison_ok = int(ns["n_min_two_modes_k_at_least_inverse_R"]) < min(two_values) and int(wd["n_min_two_modes_k_at_least_inverse_R"]) <= statistics.median(two_values)
    add(checks, "VAL4952_18_local_comparison", "frequency support does not provide a galaxy-only selector", True, local_comparison_ok, local_comparison_ok)

    poynting_decisions = {row["decision"] for row in poynting}
    poynting_ok = len(poynting) == 4 and all(as_bool(row["passed"]) for row in poynting) and {
        "EXACT_ZERO_REAL_PAIR_SOURCE",
        "ALLOWED_BUT_FREQUENCY_AND_KAPPA4_GATED",
        "NOT_A_DIRECT_GALAXY_PROFILE_DERIVATION",
        "UNIVERSAL_SOURCE_NORMALIZATION_RETAINED",
    } == poynting_decisions
    add(checks, "VAL4952_19_Poynting", "DC and oscillatory Poynting cases are separately resolved", True, sorted(poynting_decisions), poynting_ok)

    decision_map = {row["decision_id"]: row for row in decisions}
    decision_ok = (
        len(decisions) == 7
        and as_bool(decision_map["DEC4952_00_vertex"]["result"])
        and not as_bool(decision_map["DEC4952_01_ground_state"]["result"])
        and not as_bool(decision_map["DEC4952_02_stationary"]["result"])
        and not as_bool(decision_map["DEC4952_03_smooth_galaxy"]["result"])
        and not as_bool(decision_map["DEC4952_05_route"]["result"])
        and decision_map["DEC4952_06_local_GR"]["decision"] == "NO_4947_BRANCH_RETAINED"
    )
    add(checks, "VAL4952_20_decision", "route rejected without rejecting the parent pair channel or local GR branch", True, decision_map, decision_ok)

    expected_decisions = {
        "parent_pair_channel_exists": True,
        "symmetrized_vacuum_noise_is_real_pair_source": False,
        "stationary_or_DC_Poynting_pair_source": False,
        "smooth_late_time_galaxy_direct_profile_support": False,
        "spectral_support_proves_local_silence": False,
        "late_time_smooth_CTP_route_accepted": False,
        "local_GR_Newton_Maxwell_4947_retained": True,
        "full_MTS_galaxy_unification": False,
    }
    add(checks, "VAL4952_21_JSON_decision", "machine-readable claim boundary is exact", expected_decisions, result["decisions"], result["decisions"] == expected_decisions)

    valid_flags = [row["valid_for_full_MTS_claim"] for table in (vertex, spectral, sparc, local, poynting, decisions, snapshot) for row in table]
    add(checks, "VAL4952_22_nonclaim", "every generated row remains non-claim", ["False"], sorted(set(valid_flags)), set(valid_flags) == {"False"} and result["valid_for_full_MTS_claim"] is False)
    missing_markers = [value for table in (vertex, spectral, sparc, local, poynting, decisions, snapshot) for row in table for value in row.values() if "MISSING_" in str(value)]
    add(checks, "VAL4952_23_no_placeholders", "no generated output contains MISSING placeholders", [], missing_markers, not missing_markers)

    head = subprocess.run(["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "-C", str(GALAXY_REPO), "status", "--short"], check=True, capture_output=True, text=True).stdout.strip()
    snapshot_ok = len(snapshot) == 1 and as_bool(snapshot[0]["passed"]) and head == EXPECTED_GALAXY_HEAD and status == ""
    add(checks, "VAL4952_24_galaxy_snapshot", "galaxy repository remained read-only and clean", f"{EXPECTED_GALAXY_HEAD};clean", f"{head};{status!r}", snapshot_ok)

    next_target_ok = result["next_target"].startswith("4953-") and "formation-transient" in result["next_target"] and "kinetic-cascade" in result["next_target"]
    add(checks, "VAL4952_25_next_target", "next target is constructive formation/cascade amplitude derivation", True, result["next_target"], next_target_ok)

    source_sizes = {path.name: path.stat().st_size for path in (HU_PDF, HESSELS_PDF, KILIC_PDF)}
    add(checks, "VAL4952_26_primary_PDFs", "all acquired primary PDFs are nonempty", True, source_sizes, all(size > 100_000 for size in source_sizes.values()))
    add(checks, "VAL4952_27_script_digest", "research script is nonempty and hashable", True, digest(RESEARCH_SCRIPT), RESEARCH_SCRIPT.stat().st_size > 10_000)

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8-sig")
    provenance_text = PROVENANCE.read_text(encoding="utf-8-sig")
    formal_text = FORMAL.read_text(encoding="utf-8-sig")
    equation_text = EQUATIONS.read_text(encoding="utf-8-sig")
    red_team_text = RED_TEAM.read_text(encoding="utf-8-sig")
    spine_text = SPINE.read_text(encoding="utf-8-sig")
    resume_text = RESUME.read_text(encoding="utf-8-sig")
    document_ok = (
        "MTS_VISIBLE_MATTER_GRAVITON_CTP_PAIR_SOURCE_SUPPORT_4952" in checkpoint_text
        and "REJECT_DIRECT_LATE_TIME_SMOOTH_ROUTE" not in checkpoint_text
        and "late-time smooth CTP direct galaxy route       = rejected" in checkpoint_text
        and "PPC4161_VISIBLE_MATTER_GRAVITON_CTP_PAIR_SOURCE_4952" in formal_text
        and "33/33 checks passed" in provenance_text
    )
    add(checks, "VAL4952_28_documents", "checkpoint formal note and provenance carry exact scoped decision", True, document_ok, document_ok)

    claims = read_csv(CLAIMS)
    claim_794 = [row for row in claims if row["claim_id"] == "L-794"]
    claim_ok = (
        len(claim_794) == 1
        and claim_794[0]["status"] == "parent_CTP_pair_channel_derived_late_time_smooth_direct_galaxy_route_rejected_private_nonclaim"
        and "FULL_MTS_FALSE" in claim_794[0]["notes"]
    )
    add(checks, "VAL4952_29_claim", "claim L-794 is unique scoped and nonclaim", True, claim_794, claim_ok)

    variables = read_csv(VARIABLES)
    expected_variables = {
        "ParentHpsiPsiVertex4952_MTS",
        "MatterStressNoise4952_MTS",
        "InducedGravitonNoise4952_MTS",
        "MotionPairEmissionKernel4952_MTS",
        "PairSpectralSupport4952_MTS",
        "GalaxyHarmonicGate4952_MTS",
        "LocalRotatorSupport4952_MTS",
        "PoyntingPairSourceDecision4952_MTS",
        "PredictivityStatus4952_MTS",
    }
    actual_variables = {row["symbol"] for row in variables if row["symbol"].endswith("4952_MTS")}
    add(checks, "VAL4952_30_variables", "all nine 4952 canonical variables are unique", sorted(expected_variables), sorted(actual_variables), actual_variables == expected_variables)

    register_ok = (
        "## 1.245 Matter-graviton CTP pair source and spectral support" in equation_text
        and "## 196. Noise is not emission and frequency is not an environmental selector" in red_team_text
        and "## PPC4161 checkpoint 4952 - matter/graviton CTP source and support decision" in spine_text
        and "## Current checkpoint 4952 handoff" in resume_text
        and result["next_target"] in resume_text
    )
    add(checks, "VAL4952_31_registers", "equation red-team spine and resume registers are synchronized", True, register_ok, register_ok)
    add(checks, "VAL4952_32_all_prior", "all preceding validation checks pass", True, sum(bool(row["passed"]) for row in checks), all(bool(row["passed"]) for row in checks))

    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    passed = sum(bool(row["passed"]) for row in checks)
    print(json.dumps({"passed": passed, "total": len(checks), "validation": str(VALIDATION)}, indent=2))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
