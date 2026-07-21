from __future__ import annotations

import csv
import json
import math
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

import Y5_R2FR_4888_bath_kubo_backreacted_cosmology as research  # noqa: E402


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
    output_sources = [
        (
            "SRC4888_10_checkpoint",
            POST
            / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md",
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
        (
            "SRC4888_11_formal_note",
            FORMAL
            / "904-PPC4161-bath-Kubo-backreacted-memory-cosmology.md",
            "PPC4161_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
        (
            "SRC4888_12_claim",
            FORMAL / "02-claims-register.csv",
            "L-730",
        ),
        (
            "SRC4888_13_variables",
            FORMAL / "04-variable-audit.csv",
            "bathKubo_4888_MTS",
        ),
        (
            "SRC4888_14_equations",
            FORMAL / "05-equation-register.md",
            "1.181 Bath Kubo matching and conserved backreacted memory",
        ),
        (
            "SRC4888_15_redteam",
            FORMAL / "06-consistency-red-team.md",
            "132. A bare principal block is not the coupled characteristic cone",
        ),
        (
            "SRC4888_16_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4888",
        ),
        (
            "SRC4888_17_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_BATH_KUBO_BACKREACTED_COSMOLOGY_4888",
        ),
    ]
    for source_id, path, marker in output_sources:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "generated_local_text",
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
    spectral = sections["spectral_matching"]
    characteristics = sections["characteristics"]
    background = sections["backreacted_FLRW"]
    growth = sections["growth_limit"]
    likelihood = sections["likelihood"]
    return {
        "SPECTRAL_MATCHING": tagged([spectral]),
        "STRESS_OWNER": tagged([sections["stress_owner"]]),
        "CHARACTERISTICS": tagged(characteristics["rows"]),
        "CHARACTERISTIC_SUMMARY": tagged(
            [summary_row(characteristics, {"rows"})]
        ),
        "BACKREACTED_BRANCHES": tagged(background["rows"]),
        "BACKREACTED_SUMMARY": tagged(
            [summary_row(background, {"rows"})]
        ),
        "GROWTH_LIMIT": tagged(growth["rows"]),
        "GROWTH_SUMMARY": tagged([summary_row(growth, {"rows"})]),
        "LIKELIHOOD_BASELINES": tagged(likelihood["baseline_rows"]),
        "LIKELIHOOD_BRANCHES": tagged(likelihood["branch_rows"]),
        "INFORMATION_CRITERIA": tagged(likelihood["information_rows"]),
        "LIKELIHOOD_SUMMARY": tagged(
            [
                summary_row(
                    likelihood,
                    {"baseline_rows", "branch_rows", "information_rows"},
                )
            ]
        ),
        "ARBITRATION": tagged([sections["arbitration"]]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
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
    spectral = sections["spectral_matching"]
    stress = sections["stress_owner"]
    characteristics = sections["characteristics"]
    background = sections["backreacted_FLRW"]
    growth = sections["growth_limit"]
    likelihood = sections["likelihood"]
    arbitration = sections["arbitration"]
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4887_VALIDATION.csv")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-730"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    expected_statuses = {
        "Kphitheta_bath_MTS": (
            "derived_zero_frequency_cross_Kubo_matching_numeric_spectrum_open"
        ),
        "Cdiag_bath_4888_MTS": (
            "mandatory_positive_semidefinite_diagonal_susceptibilities"
        ),
        "Tsigma_memory_MTS": (
            "covariant_interaction_stress_and_clock_current_derived"
        ),
        "Rmix_clock_memory_MTS": (
            "gradient_stable_benchmark_coupled_cone_shift_derived"
        ),
        "Eback_memory_4888_MTS": (
            "three_fully_backreacted_conserved_background_rays"
        ),
        "growth_smooth_4888_MTS": (
            "controlled_smooth_memory_dust_limit_not_full_kernel"
        ),
        "likelihood_4888_MTS": (
            "real_PantheonPlus_DESI_DR2_fixed_row_smoke_nonclaim"
        ),
        "bathKubo_4888_MTS": (
            "background_viable_coupled_causal_front_and_binary_gate_open"
        ),
    }
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in expected_statuses
    }
    checkpoint = (
        POST
        / "4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "904-PPC4161-bath-Kubo-backreacted-memory-cosmology.md"
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
        OUTPUT / f"P8_Y5_R2FR_4888_{name}.csv" for name in groups
    ]
    branch_by_target = {
        row["target_Omega_memory_today"]: row
        for row in background["rows"]
    }
    likelihood_lookup = {
        (row["branch"], row["target_Omega_memory_today"]): row
        for row in likelihood["branch_rows"]
    }
    fixed_lookup = {
        row["branch"]: row
        for row in likelihood["baseline_rows"]
        if row["model"] == "LCDM_fixed_Omega_m_0p315"
    }
    rows = [
        check(
            "VAL4888_00_calculation",
            calculation["all_checks_pass"],
            "spectral stress characteristic background growth and likelihood sections pass",
        ),
        check(
            "VAL4888_01_sources",
            len(sources) == 18
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"source rows={len(sources)}",
        ),
        check(
            "VAL4888_02_prior",
            bool(prior) and all(row["status"] == "PASS" for row in prior),
            "4887 validation remains green",
        ),
        check(
            "VAL4888_03_Kubo_formula",
            spectral["passed"]
            and "sum_a c_a d_a/Omega_a^2" in spectral["sigma_matching"],
            "closed bath cross susceptibility matches sigma_theta",
        ),
        check(
            "VAL4888_04_Kubo_independence",
            not spectral["sigma_fixed_by_gamma_alone"]
            and not spectral["numeric_parent_prediction_complete"],
            "gamma auto spectrum does not fabricate cross spectral data",
        ),
        check(
            "VAL4888_05_diagonal_terms",
            "C_phi_phi" in spectral["local_effective_action"]
            and "C_theta_theta" in spectral["local_effective_action"]
            and "<=" in spectral["cauchy_schwarz"],
            "mandatory diagonal response and Cauchy-Schwarz retained",
        ),
        check(
            "VAL4888_06_spectral_example",
            spectral["constructive_example_positive_semidefinite"]
            and 0.78 < spectral["normalized_benchmark_correlation"] < 0.79,
            "healthy two-mode normalized coupling example",
        ),
        check(
            "VAL4888_07_stress_owner",
            stress["passed"]
            and "T_sigma_mn" in stress["interaction_stress"]
            and "J_Theta" in stress["clock_current"],
            "interaction stress and clock current varied",
        ),
        check(
            "VAL4888_08_background_pressure",
            stress["homogeneous_interaction_density"] == "rho_sigma=0"
            and "p_sigma=-" in stress["homogeneous_interaction_pressure"],
            "linear velocity term has zero density but nonzero pressure",
        ),
        check(
            "VAL4888_09_total_conservation",
            "=0" in stress["total_continuity"]
            and "on shell zero" in stress["diffeomorphism_identity"],
            "bath heating and interaction work close total conservation",
        ),
        check(
            "VAL4888_10_characteristic_stability",
            characteristics["passed"]
            and characteristics["mixing_ratio"] < 1.0
            and all(
                row["no_gradient_instability"]
                for row in characteristics["rows"]
            ),
            "coupled roots remain positive",
        ),
        check(
            "VAL4888_11_coupled_cone_correction",
            characteristics["bare_phi_principal_block_unchanged"]
            and not characteristics["coupled_public_cone_unchanged"],
            "4887 bare-block statement is narrowed rather than repeated",
        ),
        check(
            "VAL4888_12_upper_root",
            all(
                row["public_cone_exceeded_low_energy"]
                for row in characteristics["rows"]
            )
            and "c_plus^2>max" in characteristics["upper_root_theorem"],
            "nonzero dynamical clock mixing raises the upper low-energy cone",
        ),
        check(
            "VAL4888_13_background_rows",
            background["passed"]
            and len(background["rows"]) == 3
            and set(branch_by_target) == set(research.TARGETS),
            "three predeclared branches backreacted",
        ),
        check(
            "VAL4888_14_background_targets",
            all(
                abs(
                    row["Omega_memory_today"]
                    / row["target_Omega_memory_today"]
                    - 1.0
                )
                < 1.0e-8
                for row in background["rows"]
            ),
            "present bath memory and H0 closure shot simultaneously",
        ),
        check(
            "VAL4888_15_Friedmann_conservation",
            all(
                row["maximum_abs_Friedmann_derivative_residual"] < 1.0e-10
                and row["maximum_relative_total_continuity_residual"]
                < 1.0e-10
                for row in background["rows"]
            ),
            "constraint Raychaudhuri and total continuity agree",
        ),
        check(
            "VAL4888_16_bath_heating",
            branch_by_target[1.0e-2]["bath_heating_compensation_fraction"]
            > 0.018
            and branch_by_target[1.0e-4]["bath_heating_compensation_fraction"]
            < 2.0e-5,
            "damping energy is deposited into the bath rather than lost",
        ),
        check(
            "VAL4888_17_growth_limit",
            growth["passed"]
            and len(growth["rows"]) == 12
            and not growth["full_coupled_perturbation_likelihood"],
            "controlled smooth-memory dust limit is scoped",
        ),
        check(
            "VAL4888_18_growth_size",
            growth["maximum_abs_fractional_D_shift"] < 0.003
            and growth["maximum_abs_fractional_f_shift"] < 0.005,
            "predeclared branches have sub-percent smooth-limit growth shifts",
        ),
        check(
            "VAL4888_19_likelihood_execution",
            likelihood["passed"]
            and len(likelihood["baseline_rows"]) == 8
            and len(likelihood["branch_rows"]) == 6,
            "two SN branches three baselines and three MTS rows executed",
        ),
        check(
            "VAL4888_20_data_shapes",
            {row["n_data"] for row in likelihood["baseline_rows"]}
            == {1637, 1714},
            "Pantheon no-SH0ES 1624 SH0ES 1701 and DESI 13 rows",
        ),
        check(
            "VAL4888_21_baseline_fits",
            all(row["success"] and not row["edge_flag"] for row in likelihood["baseline_rows"]),
            "all baseline fits converge without prior edges",
        ),
        check(
            "VAL4888_22_fixed_row_delta",
            -2.4
            < likelihood_lookup[("no_sh0es", 1.0e-2)]["chi2_total"]
            - fixed_lookup["no_sh0es"]["chi2_total"]
            < -2.2
            and -3.8
            < likelihood_lookup[("sh0es", 1.0e-2)]["chi2_total"]
            - fixed_lookup["sh0es"]["chi2_total"]
            < -3.4,
            "percent row modestly improves matched fixed LCDM chi2",
        ),
        check(
            "VAL4888_23_information_scope",
            len(likelihood["information_rows"]) == 48
            and all(
                not row["stable_evidence_allowed"]
                for row in likelihood["information_rows"]
            ),
            "conditional and conservative parameter counts are both reported",
        ),
        check(
            "VAL4888_24_arbitration",
            arbitration["passed"]
            and not arbitration["expansion_source_demoted"]
            and not arbitration["expansion_source_promoted_to_parent_prediction"],
            "background route retained without causal or parent promotion",
        ),
        check(
            "VAL4888_25_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "bath_Kubo_formula_stress_backreaction_and_real_data_smoke_derived_numeric_cross_spectrum_causal_front_and_binary_open_private_nonclaim",
            "L-730 unique and nonclaim scope locked",
        ),
        check(
            "VAL4888_26_variables",
            all(
                variable_counts[symbol] == 1
                and variables[symbol]["status"] == status
                for symbol, status in expected_statuses.items()
            ),
            "eight 4888 variables unique and status locked",
        ),
        check(
            "VAL4888_27_documents",
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888" in checkpoint
            and "PPC4161_BATH_KUBO_BACKREACTED_COSMOLOGY_4888"
            in formal_note,
            "checkpoint and formal-note markers",
        ),
        check(
            "VAL4888_28_registers",
            "1.181 Bath Kubo matching and conserved backreacted memory"
            in equations
            and "132. A bare principal block is not the coupled characteristic cone"
            in redteam
            and "PPC4161 checkpoint 4888" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4888_29_resume",
            "PPC4161_BATH_KUBO_BACKREACTED_COSMOLOGY_4888" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4888_30_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4888_31_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private nonclaim",
        ),
        check(
            "VAL4888_32_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4888_33_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4888_bath_kubo_backreacted_cosmology.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4888_bath_kubo_backreacted_cosmology_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4888_34_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4888_35_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4889 nonlocal causal-front and binary target selected",
        ),
    ]
    rows.append(
        check(
            "VAL4888_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4888_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4888_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4888_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4888_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4888_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
