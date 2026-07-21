from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4954"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4954_VALIDATION.csv"

RESEARCH = POST / "scripts" / "Y5_R2FR_4954_offshell_X2_X3_number_change_gate.py"
CHECKPOINT = POST / "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL = ROOT / "formalization-workbench" / "970-PPC4161-finite-time-X2-X3-number-change-decision.md"
CLAIMS = ROOT / "formalization-workbench" / "02-claims-register.csv"
VARIABLES = ROOT / "formalization-workbench" / "04-variable-audit.csv"
EQUATIONS = ROOT / "formalization-workbench" / "05-equation-register.md"
RED_TEAM = ROOT / "formalization-workbench" / "06-consistency-red-team.md"
SPINE = ROOT / "formalization-workbench" / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

RESULT = SOURCE / "offshell_X2_X3_number_change_results.json"
PREBOLTZMANN = SOURCE / "finite_time_2PI_preBoltzmann_kernel.csv"
GAUSSIAN_COEFFICIENT = SOURCE / "gaussian_13_collinear_coefficient.csv"
GAUSSIAN_REPLICATES = SOURCE / "gaussian_13_collinear_QMC_replicates.csv"
SPARC = SOURCE / "SPARC_finite_time_and_controlled_24_gate.csv"
AMPLITUDE = SOURCE / "X2_X3_24_amplitude_completion.csv"
PHASE_REPLICATES = SOURCE / "X2_X3_24_phase_space_QMC_replicates.csv"
LOCAL = SOURCE / "local_compact_offshell_preparation_gate.csv"
DECISION = SOURCE / "offshell_X2_X3_route_decision.csv"

MARKER = "MTS_4954_OFFSHELL_X2_X3_NUMBER_CHANGE_GATE"
VALIDATION_MARKER = "MTS_4954_INDEPENDENT_VALIDATION"
HBAR_EV_S = 6.582_119_569e-16
A_MAX = 1090.92
G_MAX = 3.0 * math.pi / 5.0
C22 = 7.0 / (5.0 * math.pi)
HIGH_CASES = {
    "white_dwarf_fundamental_pair_quantum",
    "neutron_star_fundamental_pair_quantum",
    "one_GeV_quantum",
    "UHE_1e20_eV_quantum",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def close(left: float, right: float, relative: float = 3.0e-12, absolute: float = 0.0) -> bool:
    return math.isclose(left, right, rel_tol=relative, abs_tol=absolute)


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
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    execution = subprocess.run(
        [sys.executable, str(RESEARCH)],
        cwd=POST,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    add(checks, "VAL4954_00_research", "research runner completes", 0, execution.returncode, execution.returncode == 0)

    outputs = [RESULT, PREBOLTZMANN, GAUSSIAN_COEFFICIENT, GAUSSIAN_REPLICATES, SPARC, AMPLITUDE, PHASE_REPLICATES, LOCAL, DECISION]
    documents = [RESEARCH, CHECKPOINT, PROVENANCE, FORMAL, CLAIMS, VARIABLES, EQUATIONS, RED_TEAM, SPINE, RESUME]
    missing = [str(path) for path in outputs + documents if not path.is_file()]
    add(checks, "VAL4954_01_paths", "all source, output and document paths exist", [], missing, not missing)
    if missing or execution.returncode != 0:
        VALIDATION.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
            writer.writeheader()
            writer.writerows(checks)
        return 1

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    preboltzmann = read_csv(PREBOLTZMANN)
    gaussian_derivation = read_csv(GAUSSIAN_COEFFICIENT)
    gaussian_replicates = read_csv(GAUSSIAN_REPLICATES)
    sparc = read_csv(SPARC)
    amplitude = read_csv(AMPLITUDE)
    phase_replicates = read_csv(PHASE_REPLICATES)
    local = read_csv(LOCAL)
    decisions = read_csv(DECISION)
    tables = (preboltzmann, gaussian_derivation, gaussian_replicates, sparc, amplitude, phase_replicates, local, decisions)

    marker_ok = result["checkpoint_marker"] == MARKER and all(row["checkpoint_marker"] == MARKER for table in tables for row in table)
    add(checks, "VAL4954_02_marker", "result and every evidence row use the checkpoint marker", MARKER, result["checkpoint_marker"], marker_ok)
    nonclaim_ok = all(not as_bool(row["valid_for_full_MTS_claim"]) for table in tables for row in table)
    add(checks, "VAL4954_03_nonclaim", "all evidence rows remain private nonclaim", True, nonclaim_ok, nonclaim_ok)

    hash_failures = [path for path, expected in result["source_hashes"].items() if not Path(path).is_file() or digest(Path(path)) != expected]
    add(checks, "VAL4954_04_hashes", "all source locks independently recompute", [], hash_failures, result["source_hashes_match"] and not hash_failures)
    clauses_ok = all(result["source_clause_checks"].values())
    add(checks, "VAL4954_05_clauses", "all parent and 2PI source clauses are located", True, result["source_clause_checks"], clauses_ok)

    channel_map = {row["channel"]: row["energy_combination"] for row in preboltzmann}
    expected_channels = {
        "0<->4": "DeltaE=Ep+Eq+Ek+Es",
        "1<->3": "DeltaE=Ep+Eq+Ek-Es",
        "2<->2": "DeltaE=Ep+Eq-Ek-Es",
        "3<->1": "DeltaE=Ep-Eq-Ek-Es",
    }
    add(checks, "VAL4954_06_channels", "four finite-time sign channels are exact", expected_channels, channel_map, all(channel_map.get(key) == value for key, value in expected_channels.items()))
    preboltzmann_ok = len(preboltzmann) == 7 and all(as_bool(row["passed"]) for row in preboltzmann)
    add(checks, "VAL4954_07_preBoltzmann", "all finite-time kernel rows pass", "7 pass", len(preboltzmann), preboltzmann_ok)

    angular_values = [float(row["mean_collinear_angular_kernel_squared"]) for row in gaussian_replicates]
    angular_mean = statistics.mean(angular_values)
    angular_error = statistics.stdev(angular_values) / math.sqrt(len(angular_values))
    coefficient_13 = angular_mean / (24.0 * math.pi**3)
    coefficient_13_error = angular_error / (24.0 * math.pi**3)
    gaussian_shape = len(gaussian_replicates) == 4 and all(int(row["event_count"]) == 2**18 and as_bool(row["all_finite"]) for row in gaussian_replicates)
    add(checks, "VAL4954_08_gaussian_shape", "four independent finite Gaussian replicas exist", "4 x 2^18", len(gaussian_replicates), gaussian_shape)
    add(checks, "VAL4954_09_C13", "C13 independently recomputes from angular mean", coefficient_13, result["finite_time"]["C13_Gaussian"], close(coefficient_13, result["finite_time"]["C13_Gaussian"]))
    add(checks, "VAL4954_10_C13_error", "C13 standard error independently recomputes", coefficient_13_error, result["finite_time"]["C13_Gaussian_standard_error"], close(coefficient_13_error, result["finite_time"]["C13_Gaussian_standard_error"]))
    radial_integral = 0.25 * 4.0**3 * math.gamma(3.0)
    add(checks, "VAL4954_11_radial", "analytic Gaussian radial integral equals 32", 32.0, radial_integral, radial_integral == 32.0)
    unitarity_numerator = coefficient_13 * G_MAX**2
    add(checks, "VAL4954_12_unitarity", "smooth-preparation numerator uses the 4953 unitarity ceiling", unitarity_numerator, result["finite_time"]["unitarity_numerator_C13_gmax2"], close(unitarity_numerator, result["finite_time"]["unitarity_numerator_C13_gmax2"]))
    gaussian_rows_ok = len(gaussian_derivation) == 6 and all(as_bool(row["passed"]) for row in gaussian_derivation)
    add(checks, "VAL4954_13_gaussian_rows", "all analytic preparation rows pass", "6 pass", len(gaussian_derivation), gaussian_rows_ok)

    exchange_values = [float(row["mean_exchange_squared"]) for row in phase_replicates]
    cross_values = [float(row["mean_exchange_contact"]) for row in phase_replicates]
    contact_values = [float(row["mean_contact_squared"]) for row in phase_replicates]
    mean_exchange = statistics.mean(exchange_values)
    mean_cross = statistics.mean(cross_values)
    mean_contact = statistics.mean(contact_values)
    phase_volume = 1.0 / (24_576.0 * math.pi**5)
    head_on_factor = phase_volume * 4.0**7 / (2.0 * math.factorial(4))
    coefficient_0 = head_on_factor * mean_exchange
    coefficient_1 = 2.0 * head_on_factor * mean_cross
    coefficient_2 = head_on_factor * mean_contact
    ratio_minimum = -coefficient_1 / (2.0 * coefficient_2)
    coefficient_minimum = coefficient_0 - coefficient_1**2 / (4.0 * coefficient_2)
    phase_shape = len(phase_replicates) == 8 and all(int(row["event_count"]) == 2**16 and as_bool(row["all_finite"]) for row in phase_replicates)
    phase_accuracy = all(float(row["RAMBO_sum_error_max"]) < 1.0e-12 and float(row["RAMBO_mass_shell_error_max"]) < 1.0e-12 for row in phase_replicates)
    add(checks, "VAL4954_14_phase_shape", "eight independent RAMBO replicas exist", "8 x 2^16", len(phase_replicates), phase_shape)
    add(checks, "VAL4954_15_phase_accuracy", "RAMBO rows conserve four-momentum and remain massless", "<1e-12", phase_accuracy, phase_accuracy)
    add(checks, "VAL4954_16_C0", "exchange coefficient independently recomputes", coefficient_0, result["on_shell_24"]["C0"], close(coefficient_0, result["on_shell_24"]["C0"]))
    add(checks, "VAL4954_17_C1", "interference coefficient independently recomputes", coefficient_1, result["on_shell_24"]["C1"], close(coefficient_1, result["on_shell_24"]["C1"]))
    add(checks, "VAL4954_18_C2", "contact coefficient independently recomputes", coefficient_2, result["on_shell_24"]["C2"], close(coefficient_2, result["on_shell_24"]["C2"]))
    minimum_ok = close(ratio_minimum, result["on_shell_24"]["r3_minimum"]) and close(coefficient_minimum, result["on_shell_24"]["C_minimum"]) and coefficient_minimum > 0.0
    add(checks, "VAL4954_19_minimum", "phase-integrated X3 interference minimum stays positive", ">0", coefficient_minimum, minimum_ok)
    ratio_prefactor = coefficient_0 / C22
    add(checks, "VAL4954_20_ratio", "exchange 2-to-4 over 2-to-2 prefactor independently recomputes", ratio_prefactor, result["on_shell_24"]["exchange_24_to_22_prefactor"], close(ratio_prefactor, result["on_shell_24"]["exchange_24_to_22_prefactor"]))
    combinatorics_ok = math.comb(5, 2) == result["on_shell_24"]["partitions_3_3"] and math.factorial(6) // (2**3 * math.factorial(3)) == result["on_shell_24"]["perfect_matchings_6"]
    add(checks, "VAL4954_21_combinatorics", "ten 3+3 partitions and fifteen perfect matchings are complete", "10;15", f"{result['on_shell_24']['partitions_3_3']};{result['on_shell_24']['perfect_matchings_6']}", combinatorics_ok)
    amplitude_ok = len(amplitude) == 7 and all(as_bool(row["passed"]) for row in amplitude) and any(row["status"] == "ONE_COEFFICIENT_C_ONLY_24_ROUTE_INCOMPLETE" for row in amplitude)
    add(checks, "VAL4954_22_amplitude", "all six-point structure rows pass and X3 is mandatory", "7 pass", len(amplitude), amplitude_ok)

    formula_failures = 0
    for row in sparc:
        radius = float(row["outer_radius_m"])
        velocity = float(row["outer_velocity_m_s"])
        energy = float(row["injection_energy_eV"])
        profile_energy = float(row["profile_energy_eV"])
        dynamical_time = radius / velocity
        time_energy = energy * dynamical_time / HBAR_EV_S
        probability = coefficient_13 * G_MAX**2 / time_energy**4
        remaining = max(1.0, (energy / profile_energy) / A_MAX)
        required_log = math.log(remaining)
        density = float(row["required_density_eV4"])
        occupancy = 0.0 if density == 0.0 else 2.0 * math.pi**2 * density / energy**4
        if density == 0.0:
            envelope = 0.0
        elif occupancy >= 1.0:
            envelope = 2.0 * time_energy * min(1.0, energy**4 / density) ** 2
        else:
            envelope = 2.0 * (density / energy**4) * time_energy
        if not (
            close(float(row["dynamical_preparation_time_s"]), dynamical_time)
            and close(float(row["E_tau_over_hbar"]), time_energy)
            and close(float(row["P13_single_preparation_at_22_unitarity_max"]), probability)
            and close(float(row["remaining_multiplicity_after_Amax"]), remaining)
            and close(float(row["required_log_multiplicity_after_Amax"]), required_log, absolute=1.0e-300)
            and close(float(row["one_shell_occupancy_proxy"]), occupancy, absolute=1.0e-300)
            and close(float(row["unit_six_point_controlled_log_gain_envelope"]), envelope, absolute=1.0e-300)
        ):
            formula_failures += 1
    add(checks, "VAL4954_23_sparc_formulas", "every galaxy preparation and controlled-envelope row recomputes", 0, formula_failures, formula_failures == 0)
    add(checks, "VAL4954_24_sparc_shape", "six injection cases exist for each of 175 public galaxies", 1050, len(sparc), len(sparc) == 1050)

    high = [row for row in sparc if as_bool(row["positive_outer_residual_target"]) and row["injection_case"] in HIGH_CASES]
    finite_failures = sum(not as_bool(row["finite_preparation_can_close_deficit"]) for row in high)
    controlled_failures = sum(not as_bool(row["controlled_envelope_can_close_deficit"]) for row in high)
    add(checks, "VAL4954_25_finite_gate", "all positive high-frequency rows fail smooth preparation", "692/692", f"{finite_failures}/{len(high)}", len(high) == 692 and finite_failures == 692)
    add(checks, "VAL4954_26_controlled_gate", "all positive high-frequency rows fail the generous controlled envelope", "692/692", f"{controlled_failures}/{len(high)}", len(high) == 692 and controlled_failures == 692)
    maxima_ok = close(max(float(row["P13_single_preparation_at_22_unitarity_max"]) for row in high), result["execution"]["finite_preparation_probability_max_high_frequency"]) and close(max(float(row["unit_six_point_controlled_log_gain_envelope"]) for row in high), result["execution"]["controlled_envelope_log_gain_max_high_frequency"])
    add(checks, "VAL4954_27_maxima", "reported high-frequency maxima independently reproduce", True, maxima_ok, maxima_ok)

    local_failures = 0
    for row in local:
        time_energy = float(row["fundamental_pair_quantum_energy_eV"]) * float(row["preparation_observation_time_s"]) / HBAR_EV_S
        probability = coefficient_13 * G_MAX**2 / time_energy**4
        if not close(float(row["E_T_over_hbar"]), time_energy) or not close(float(row["P13_single_preparation_at_22_unitarity_max"]), probability):
            local_failures += 1
    add(checks, "VAL4954_28_local", "both compact smooth-preparation comparators recompute", "2 rows;0 failures", f"{len(local)} rows;{local_failures} failures", len(local) == 2 and local_failures == 0)

    decision_statuses = {row["status"] for row in decisions}
    required_statuses = {
        "FINITE_TIME_KERNEL_DERIVED",
        "SHARP_SWITCH_ROUTE_REJECTED",
        "SMOOTH_FINITE_PREPARATION_ROUTE_REJECTED",
        "EXCHANGE_ONLY_24_DERIVED",
        "MANDATORY_X3_PARENT_COORDINATE_IDENTIFIED",
        "CONTROLLED_HIGH_FREQUENCY_ROUTE_REJECTED",
        "STRONG_NONQUASIPARTICLE_ROUTE_OPEN",
        "PARENT_SIX_DERIVATIVE_FLOW_NEXT",
        "4947_LOCAL_BRANCH_RETAINED",
        "FULL_MTS_PROMOTION_BLOCKED",
    }
    add(checks, "VAL4954_29_decisions", "decision table contains every required route status", sorted(required_statuses), sorted(decision_statuses), len(decisions) == 10 and required_statuses == decision_statuses)
    result_decision_ok = result["decision"]["X2_exchange_24"] == "DERIVED" and not result["decision"]["X2_only_complete_24"] and result["decision"]["mandatory_next_coordinate"] == "d3_X3" and result["decision"]["strong_nonquasiparticle_X2_X3_2PI"] == "OPEN" and not result["decision"]["full_MTS"]
    add(checks, "VAL4954_30_result", "result keeps X3 and strong 2PI open without full-MTS promotion", True, result["decision"], result_decision_ok)

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8")
    formal_text = FORMAL.read_text(encoding="utf-8")
    claims_text = CLAIMS.read_text(encoding="utf-8")
    variables_text = VARIABLES.read_text(encoding="utf-8")
    equations_text = EQUATIONS.read_text(encoding="utf-8")
    red_text = RED_TEAM.read_text(encoding="utf-8")
    spine_text = SPINE.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    documentation_ok = all(
        token in text
        for token, text in (
            ("MTS_OFFSHELL_X2_X3_NUMBER_CHANGE_DECISION_4954", checkpoint_text),
            ("PPC4161_FINITE_TIME_X2_X3_NUMBER_CHANGE_4954", formal_text),
            ('"L-796"', claims_text),
            ("PredictivityStatus4954_MTS", variables_text),
            ("## 1.247", equations_text),
            ("## 198.", red_text),
            ("checkpoint 4954", spine_text),
            ("Current checkpoint 4954 handoff", resume_text),
        )
    )
    add(checks, "VAL4954_31_documents", "checkpoint 4954 is synchronized across all registers", True, documentation_ok, documentation_ok)
    prohibited = ["MISSING_PARENT_INPUT", "MISSING_ARENA_PROJECTION", "FULL_MTS_TRUE"]
    corpus = "\n".join([checkpoint_text, formal_text, claims_text, variables_text, equations_text, red_text, spine_text, resume_text])
    present = [token for token in prohibited if token in corpus]
    add(checks, "VAL4954_32_prohibitions", "new synchronized text contains no placeholder or promotion marker", [], present, not present)
    provenance_ok = all(value in PROVENANCE.read_text(encoding="utf-8") for value in result["source_hashes"].values())
    add(checks, "VAL4954_33_provenance", "provenance records every locked source hash", True, provenance_ok, provenance_ok)
    pycache = list((POST / "scripts").glob("__pycache__"))
    add(checks, "VAL4954_34_pycache", "no script bytecode cache remains", [], [str(path) for path in pycache], not pycache)

    all_passed = all(as_bool(row["passed"]) for row in checks)
    add(checks, "VAL4954_35_complete", "all preceding independent checks pass", True, all_passed, all_passed)
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    return 0 if all(as_bool(row["passed"]) for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
