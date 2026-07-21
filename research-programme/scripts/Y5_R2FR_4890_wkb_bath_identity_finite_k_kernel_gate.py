from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return value


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        normalized = {key: serializable(value) for key, value in row.items()}
        normalized["valid_for_claim"] = False
        normalized["timestamp_utc"] = TIMESTAMP
        output.append(normalized)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return False
    return True


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    outputs = [
        (
            "SRC4890_05_checkpoint",
            POST
            / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md",
            "MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890",
        ),
        (
            "SRC4890_06_formal",
            FORMAL / "906-PPC4161-composite-clock-finite-k-FDT-gate.md",
            "PPC4161_COMPOSITE_CLOCK_FINITE_K_FDT_4890",
        ),
        (
            "SRC4890_07_claim",
            FORMAL / "02-claims-register.csv",
            "L-732",
        ),
        (
            "SRC4890_08_variables",
            FORMAL / "04-variable-audit.csv",
            "clockRoute_4890_MTS",
        ),
        (
            "SRC4890_09_equations",
            FORMAL / "05-equation-register.md",
            "1.183 Composite clock and finite-k SK system",
        ),
        (
            "SRC4890_10_redteam",
            FORMAL / "06-consistency-red-team.md",
            "134. A controlled microscopic chart is not a global completion",
        ),
        (
            "SRC4890_11_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4890",
        ),
        (
            "SRC4890_12_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_COMPOSITE_CLOCK_FINITE_K_FDT_4890",
        ),
        (
            "SRC4890_13_research_script",
            SCRIPTS / "Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel.py",
            "def composite_clock_identity",
        ),
        (
            "SRC4890_14_gate_script",
            SCRIPTS
            / "Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel_gate.py",
            "VAL4890_OVERALL",
        ),
    ]
    for source_id, path, marker in outputs:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "generated_local_text_or_code",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
            }
        )
    return tagged(rows)


def summary_row(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    identity = sections["identity"]
    early = sections["early_background"]
    finite_k = sections["finite_k"]
    noise = sections["noise_CMB"]
    return {
        "COMPOSITE_IDENTITY": tagged(
            [summary_row(identity, {"mass_floor_rows"})]
        ),
        "MASS_FLOORS": tagged(identity["mass_floor_rows"]),
        "EARLY_BACKGROUND": tagged(early["rows"]),
        "EARLY_BACKGROUND_SUMMARY": tagged(
            [summary_row(early, {"rows"})]
        ),
        "FINITE_K_MODES": tagged(finite_k["rows"]),
        "FINITE_K_SUMMARY": tagged(
            [summary_row(finite_k, {"rows"})]
        ),
        "NOISE_RESPONSES": tagged(noise["response_rows"]),
        "CMB_REQUIREMENTS": tagged(noise["requirements"]),
        "NOISE_CMB_SUMMARY": tagged(
            [summary_row(noise, {"response_rows", "requirements"})]
        ),
        "ARBITRATION": tagged([sections["arbitration"]]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "CMB_likelihood_allowed": noise[
                        "CMB_likelihood_allowed"
                    ],
                    "next_target": sections["arbitration"]["next_target"],
                }
            ]
        ),
    }


def validation_rows(
    calculation: dict[str, Any],
    sources: list[dict[str, Any]],
    groups: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    def check(check_id: str, condition: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    sections = calculation["sections"]
    identity = sections["identity"]
    early = sections["early_background"]
    finite_k = sections["finite_k"]
    noise = sections["noise_CMB"]
    arbitration = sections["arbitration"]
    prior_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4889_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-732"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "Zclock_pair_4890_MTS": "derived_composite_existing_degenerate_bath_pair",
        "mc_clock_4890_MTS": "lower_bound_only_parent_value_open",
        "earlyFLRW_4890_MTS": (
            "Nminus14_reshot_three_rays_overlap_below_4p88e-7"
        ),
        "thetaPert_4890_MTS": "exact_finite_k_expansion_perturbation",
        "finiteK_4890_MTS": "nine_mode_constraint_linearity_gate_pass",
        "deltaQSK_4890_MTS": "energy_conserving_linear_transfer_derived",
        "GPhixi_4890_MTS": "unit_impulse_retarded_response_computed",
        "CMBgate_4890_MTS": "blocked_bath_state_and_standard_hierarchies",
        "clockRoute_4890_MTS": "composite_identity_finite_k_FDT_pass_CMB_open",
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }
    checkpoint_path = (
        POST
        / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "906-PPC4161-composite-clock-finite-k-FDT-gate.md"
    ).read_text(encoding="utf-8")
    equations = (FORMAL / "05-equation-register.md").read_text(
        encoding="utf-8"
    )
    redteam = (FORMAL / "06-consistency-red-team.md").read_text(
        encoding="utf-8"
    )
    spine = (FORMAL / "07-unification-spine.md").read_text(
        encoding="utf-8"
    )
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(
        encoding="utf-8"
    )
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4890_{name}.csv" for name in groups
    ]
    early_by_target = {row["target"]: row for row in early["rows"]}
    finite_lookup = {
        (row["target"], row["k_h_per_Mpc"]): row
        for row in finite_k["rows"]
    }
    requirements = {
        row["requirement"]: row for row in noise["requirements"]
    }
    rows = [
        check(
            "VAL4890_00_calculation",
            calculation["all_checks_pass"],
            "identity early finite-k noise and arbitration sections pass",
        ),
        check(
            "VAL4890_01_sources",
            len(sources) == 15
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"source rows={len(sources)}",
        ),
        check(
            "VAL4890_02_prior",
            bool(prior_validation)
            and all(row["status"] == "PASS" for row in prior_validation),
            "4889 validation remains green",
        ),
        check(
            "VAL4890_03_symbolic_pair",
            identity["passed"]
            and identity["kinetic_identity_verified"]
            and identity["angular_identity_verified"],
            "Cartesian polar kinetic and angular-current identities verified",
        ),
        check(
            "VAL4890_04_composite_map",
            "X_1 grad_mu X_2" in identity["exact_composite_map"]
            and identity["derived_multiplier"] == "varrho=m_c^2 A^2",
            "U and varrho explicitly mapped to existing bath coordinates",
        ),
        check(
            "VAL4890_05_no_new_primitive",
            not identity["new_primitive_field_required"]
            and not identity["new_parent_operator_required"],
            "no new field or arena operator introduced",
        ),
        check(
            "VAL4890_06_radial_correction",
            "Box A" in identity["radial_constraint_with_correction"]
            and "A=0" in identity["zero_amplitude_domain"],
            "WKB correction and chart boundary retained",
        ),
        check(
            "VAL4890_07_bath_split",
            "excluded" in identity["coherent_continuum_split"]
            and "Kubo" in identity["sigma_owner"],
            "coherent carrier is not double counted in Ohmic continuum",
        ),
        check(
            "VAL4890_08_mass_rows",
            len(identity["mass_floor_rows"]) == 5
            and all(
                row["minimum_carrier_mass_eV"] > 0.0
                for row in identity["mass_floor_rows"]
            ),
            "five controlled spatial and temporal mass floors",
        ),
        check(
            "VAL4890_09_binary_floor",
            1.43e-17
            < identity["largest_required_mass_floor_eV"]
            < 1.44e-17,
            "eight-hour one-percent WKB floor reproduced",
        ),
        check(
            "VAL4890_10_early_rows",
            early["passed"]
            and len(early["rows"]) == 3
            and set(early_by_target) == set(research.background.TARGETS),
            "all three backgrounds reshot from N=-14",
        ),
        check(
            "VAL4890_11_early_targets",
            all(
                abs(row["memory_today"] - row["target"])
                < row["target"] * 1.0e-7
                and abs(row["clock_today"] - research.background.OMEGA_X)
                < 1.0e-9
                for row in early["rows"]
            ),
            "present target memory and clock densities retained",
        ),
        check(
            "VAL4890_12_overlap",
            max(
                row["maximum_overlap_fractional_E_shift"]
                for row in early["rows"]
            )
            < 4.9e-7,
            "late expansion overlap below 4.9e-7",
        ),
        check(
            "VAL4890_13_finite_equations",
            finite_k["passed"]
            and "delta theta" in finite_k["expansion_perturbation"]
            and "delta x_X" in finite_k["clock_energy_equation"],
            "finite-k clock memory and SK mean equations present",
        ),
        check(
            "VAL4890_14_radiation_velocity",
            "P_r,N=P_r+" in finite_k["radiation_equations"],
            "cosmic-time radiation Hubble term retained",
        ),
        check(
            "VAL4890_15_mode_grid",
            len(finite_k["rows"]) == 9
            and {row["target"] for row in finite_k["rows"]}
            == set(research.background.TARGETS)
            and {row["k_h_per_Mpc"] for row in finite_k["rows"]}
            == {1.0e-3, 1.0e-2, 3.0e-2},
            "three rays by three wavenumbers",
        ),
        check(
            "VAL4890_16_superhorizon_start",
            finite_k["largest_initial_k_over_aH"] < 7.9e-3,
            "all tested modes start superhorizon",
        ),
        check(
            "VAL4890_17_hamiltonian",
            finite_k["maximum_relative_hamiltonian_residual"] < 2.3e-16,
            "Hamiltonian constraint preserved to floating precision",
        ),
        check(
            "VAL4890_18_momentum",
            finite_k["maximum_relative_momentum_residual"] < 1.8e-3,
            "momentum constraint residual below 0.18 percent",
        ),
        check(
            "VAL4890_19_linearity",
            finite_k["maximum_linearity_residual"] < 1.0e-15
            and finite_k["all_finite"],
            "linear operator identity and finite states",
        ),
        check(
            "VAL4890_20_central_transfer",
            -0.062
            < finite_lookup[(1.0e-3, 3.0e-2)]["final_other_delta"]
            < -0.061
            and -0.056
            < finite_lookup[(1.0e-3, 3.0e-2)][
                "final_clock_fractional_delta"
            ]
            < -0.054,
            "central high sampled mode transfer reproduced",
        ),
        check(
            "VAL4890_21_noise_rows",
            noise["passed"]
            and len(noise["response_rows"]) == 4
            and all(row["finite"] for row in noise["response_rows"]),
            "four finite retarded unit-impulse responses",
        ),
        check(
            "VAL4890_22_impulse_energy",
            max(
                abs(row["initial_total_density_jump"])
                for row in noise["response_rows"]
            )
            < 1.0e-20,
            "scalar and clock impulse energy jumps cancel",
        ),
        check(
            "VAL4890_23_impulse_constraints",
            noise["maximum_impulse_hamiltonian_residual"] < 2.3e-16
            and noise["maximum_impulse_momentum_residual"] < 1.6e-3,
            "noise responses preserve global constraints",
        ),
        check(
            "VAL4890_24_noise_size",
            1.63e-5
            < noise["maximum_abs_unit_impulse_metric_response"]
            < 1.64e-5,
            "late unit-impulse metric response locked",
        ),
        check(
            "VAL4890_25_FDT",
            "coth" in noise["quantum_FDT"]
            and noise["Ohmic_classical_limit"]
            == "N=2 gamma_M T_bath in the 4873 convention",
            "quantum and classical FDT formulas retained",
        ),
        check(
            "VAL4890_26_requirements",
            len(noise["requirements"]) == 7
            and sum(row["closed"] for row in noise["requirements"]) == 2,
            "two closed and five open CMB requirements",
        ),
        check(
            "VAL4890_27_bath_state_open",
            not requirements[
                "bath_state_temperature_or_nonthermal_covariance"
            ]["closed"]
            and not requirements["coherent_pair_mass_and_fraction"][
                "closed"
            ],
            "noise amplitude and carrier preparation not fabricated",
        ),
        check(
            "VAL4890_28_hierarchy_open",
            not requirements[
                "photon_baryon_collision_and_recombination"
            ]["closed"]
            and not requirements[
                "massless_and_massive_neutrino_hierarchy"
            ]["closed"],
            "standard photon and neutrino hierarchy remains explicit",
        ),
        check(
            "VAL4890_29_CMB_block",
            not noise["CMB_likelihood_allowed"]
            and not noise["full_Einstein_Boltzmann_closed"]
            and not noise["noise_power_numerically_predictive"],
            "no CMB likelihood or stochastic power claim",
        ),
        check(
            "VAL4890_30_arbitration",
            arbitration["passed"]
            and arbitration["demotion_status"].startswith("DO_NOT_DEMOTE")
            and arbitration["CMB_status"].startswith("BLOCKED"),
            "route retained while CMB promotion stays blocked",
        ),
        check(
            "VAL4890_31_local_retained",
            arbitration["local_GR_Newton_Maxwell"]
            == "4889_STATIONARY_CORRESPONDENCE_RETAINED_UNCHANGED",
            "local correspondence not altered by cosmology extension",
        ),
        check(
            "VAL4890_32_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "composite_bath_clock_identity_and_finite_k_SK_kernel_derived_full_CMB_state_hierarchy_open_private_nonclaim",
            "L-732 unique private nonclaim status",
        ),
        check(
            "VAL4890_33_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "nine checkpoint variables unique and status locked",
        ),
        check(
            "VAL4890_34_documents",
            "MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890" in checkpoint
            and "PPC4161_COMPOSITE_CLOCK_FINITE_K_FDT_4890"
            in formal_note,
            "checkpoint and formal markers",
        ),
        check(
            "VAL4890_35_registers",
            "1.183 Composite clock and finite-k SK system" in equations
            and "134. A controlled microscopic chart is not a global completion"
            in redteam
            and "PPC4161 checkpoint 4890" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4890_36_resume",
            "PPC4161_COMPOSITE_CLOCK_FINITE_K_FDT_4890" in resume
            and NEXT_TARGET in resume,
            "resume and 4891 handoff",
        ),
        check(
            "VAL4890_37_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4890_38_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4890_39_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4890_40_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4890_41_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4890_42_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4891 hierarchy and state-normalization target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4890_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4890_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4890_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4890_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4890_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4890_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
