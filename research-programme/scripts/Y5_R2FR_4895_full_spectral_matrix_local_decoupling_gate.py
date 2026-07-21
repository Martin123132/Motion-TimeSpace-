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

import Y5_R2FR_4895_full_spectral_matrix_local_decoupling as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, complex):
        return f"{value.real:+.17g}{value.imag:+.17g}j"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), default=str
        )
    if hasattr(value, "item"):
        return value.item()
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
            "SRC4895_07_checkpoint",
            POST
            / "4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-GR-decoupling-or-bath-cosmology-retirement-gate.md",
            "MTS_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_GATE_4895",
        ),
        (
            "SRC4895_08_formal",
            FORMAL
            / "911-PPC4161-full-spectral-matrix-counterterms-and-local-decoupling.md",
            "PPC4161_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_4895",
        ),
        (
            "SRC4895_09_claim",
            FORMAL / "02-claims-register.csv",
            "L-737",
        ),
        (
            "SRC4895_10_variables",
            FORMAL / "04-variable-audit.csv",
            "LocalDecouple4895_MTS",
        ),
        (
            "SRC4895_11_equations",
            FORMAL / "05-equation-register.md",
            "1.188 Full reciprocal spectral parent",
        ),
        (
            "SRC4895_12_redteam",
            FORMAL / "06-consistency-red-team.md",
            "139. A positive spectral matrix",
        ),
        (
            "SRC4895_13_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4895",
        ),
        (
            "SRC4895_14_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_4895",
        ),
        (
            "SRC4895_15_research",
            SCRIPTS / "Y5_R2FR_4895_full_spectral_matrix_local_decoupling.py",
            "def exact_spectral_completion",
        ),
        (
            "SRC4895_16_gate",
            SCRIPTS
            / "Y5_R2FR_4895_full_spectral_matrix_local_decoupling_gate.py",
            "VAL4895_OVERALL",
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


def scalar_summary(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    spectral = sections["spectral"]
    counterterms = sections["counterterms"]
    localization = sections["localization"]
    suppression = sections["suppression"]
    local = sections["local"]
    arbitration = sections["arbitration"]
    return {
        "SPECTRAL_SUMMARY": tagged(
            [
                scalar_summary(
                    spectral, {"frequency_rows", "transform_rows"}
                )
            ]
        ),
        "FREQUENCY_RESPONSE": tagged(spectral["frequency_rows"]),
        "TRANSFORM_CHECKS": tagged(spectral["transform_rows"]),
        "COUNTERTERM_BRANCHES": tagged(counterterms["rows"]),
        "COUNTERTERM_SUMMARY": tagged(
            [scalar_summary(counterterms, {"rows"})]
        ),
        "AUXILIARY_CONSTANT_CHECKS": tagged(localization["rows"]),
        "AUXILIARY_FDT_SUMMARY": tagged(
            [scalar_summary(localization, {"rows"})]
        ),
        "LOCAL_FREQUENCY_SUPPRESSION": tagged(suppression["rows"]),
        "LOCAL_FREQUENCY_SUMMARY": tagged(
            [scalar_summary(suppression, {"rows"})]
        ),
        "LOCAL_DECOUPLING_CLAUSES": tagged(local["clauses"]),
        "LOCAL_DECOUPLING_SUMMARY": tagged(
            [scalar_summary(local, {"clauses"})]
        ),
        "COMPLETION_REQUIREMENTS": tagged(arbitration["requirements"]),
        "ARBITRATION": tagged(
            [scalar_summary(arbitration, {"requirements"})]
        ),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "current_local_cosmology_closure_status": arbitration[
                        "current_local_cosmology_closure_status"
                    ],
                    "stationary_local_status": arbitration[
                        "stationary_local_status"
                    ],
                    "next_target": arbitration["next_target"],
                    "all_checks_pass": calculation["all_checks_pass"],
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
    spectral = sections["spectral"]
    counterterms = sections["counterterms"]
    localization = sections["localization"]
    suppression = sections["suppression"]
    local = sections["local"]
    arbitration = sections["arbitration"]
    requirement_lookup = {
        row["requirement"]: row for row in arbitration["requirements"]
    }
    branch_lookup = {row["scheme"]: row for row in counterterms["rows"]}
    frequency_lookup = {
        row["omega_per_H0"]: row for row in spectral["frequency_rows"]
    }
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4894_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-737"
    ]
    variable_symbols = (
        "KR4895_MTS",
        "zBath4895_MTS",
        "Dct4895_MTS",
        "Kren4895_MTS",
        "Aux4895_MTS",
        "Noise4895_MTS",
        "CrossFilter4895_MTS",
        "LocalDecouple4895_MTS",
    )
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    new_variables = [
        row for row in variable_rows if row["symbol"] in variable_symbols
    ]
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in variable_symbols
    }
    variable_sources_exist = True
    for row in new_variables:
        for source_path in row["source_files"].split(";"):
            variable_sources_exist = (
                variable_sources_exist and (ROOT / source_path).exists()
            )
    checkpoint = (
        POST
        / "4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-GR-decoupling-or-bath-cosmology-retirement-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "911-PPC4161-full-spectral-matrix-counterterms-and-local-decoupling.md"
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
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / "P8_Y5_R2FR_4895_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4895_{name}.csv" for name in groups
        ],
    ]
    selected = branch_lookup["diagonal_clock_preserving_subtraction"]
    h0_row = frequency_lookup[1.0]
    rows = [
        check(
            "VAL4895_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4894_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4894 validation inherited",
        ),
        check(
            "VAL4895_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all prior and generated source markers exist",
        ),
        check(
            "VAL4895_02_spectral_values",
            0.1258 < spectral["C_phi_phi"] < 0.1260
            and 2.383 < spectral["q_cross"] < 2.384
            and 0.7150 < spectral["C_theta_theta"] < 0.7152,
            "inherited cutoff fixes the full static matrix",
        ),
        check(
            "VAL4895_03_double_pole",
            spectral["upper_half_plane_poles"] == 0
            and len(spectral["causal_poles"]) == 2
            and all(pole.imag < 0.0 for pole in spectral["causal_poles"]),
            "retarded kernel has only the lower-half-plane double pole",
        ),
        check(
            "VAL4895_04_transform",
            len(spectral["transform_rows"]) == 4
            and max(
                row["absolute_complex_residual"]
                for row in spectral["transform_rows"]
            )
            < 1.0e-9,
            "time kernel reproduces the analytic susceptibility",
        ),
        check(
            "VAL4895_05_spectral_identity",
            max(
                abs(row["K_scalar_imag"] - row["J_expected"])
                for row in spectral["frequency_rows"]
            )
            < 1.0e-14,
            "imaginary retarded response equals super-Drude spectrum",
        ),
        check(
            "VAL4895_06_positive_matrix",
            spectral["spectral_positive_semidefinite"]
            and spectral["spectral_rank"] == 1
            and spectral["static_eigenvalues"][0] > -1.0e-13
            and spectral["static_eigenvalues"][1] > 0.8,
            "full bath spectral matrix is rank-one positive",
        ),
        check(
            "VAL4895_07_three_counterterms",
            counterterms["passed"] and len(counterterms["rows"]) == 3,
            "all three static subtraction branches evaluated",
        ),
        check(
            "VAL4895_08_no_counterterm_rejected",
            not branch_lookup["no_counterterm"]["preserves_massless_phi"]
            and not branch_lookup["no_counterterm"][
                "preserves_zero_local_theta_squared_clock_term"
            ],
            "no-subtraction branch retains both unwanted diagonals",
        ),
        check(
            "VAL4895_09_full_Gram_rejected",
            not branch_lookup["full_Gram_subtraction"][
                "retains_sigma_cross_source"
            ],
            "full Gram subtraction erases sigma",
        ),
        check(
            "VAL4895_10_diagonal_selected",
            selected["matches_all_three_IR_conditions"]
            and selected["counterterm_phi_theta"] == 0.0
            and selected["counterterm_phi_phi"] < 0.0
            and selected["counterterm_theta_theta"] < -0.7,
            "diagonal subtraction uniquely matches all selected IR conditions",
        ),
        check(
            "VAL4895_11_counterterm_discipline",
            counterterms["spectral_positivity_unaffected"]
            and not counterterms["globally_unique_from_positivity_alone"]
            and counterterms["unique_given_selected_IR_conditions"]
            and not selected["effective_static_matrix_PSD"],
            "real counterterm and positive noise spectrum are not conflated",
        ),
        check(
            "VAL4895_12_auxiliary_rows",
            localization["passed"]
            and len(localization["rows"]) == 3
            and max(
                row["maximum_force_residual"] for row in localization["rows"]
            )
            < 1.0e-13,
            "shared auxiliaries reproduce both reciprocal constant forces",
        ),
        check(
            "VAL4895_13_auto_identity",
            "K_R(omega)-C_phi_phi" in localization["auto_memory_identity"],
            "4894 auto memory is identified as the subtracted susceptibility",
        ),
        check(
            "VAL4895_14_FDT",
            localization["same_kernel_owns_response_and_noise"]
            and "J_phi_phi" in localization["noise_matrix"],
            "response and positive noise share one spectral owner",
        ),
        check(
            "VAL4895_15_H0_cross",
            0.0595
            < h0_row["cross_susceptibility_amplitude_ratio"]
            < 0.0597,
            "full cross response is strongly non-Markovian at H0",
        ),
        check(
            "VAL4895_16_H0_friction",
            0.0035 < h0_row["friction_dissipative_ratio"] < 0.0036,
            "4894 dissipative fraction is recovered",
        ),
        check(
            "VAL4895_17_local_filter",
            suppression["passed"]
            and suppression["largest_local_cross_ratio"] < 1.0e-22,
            "all sampled local dynamical frequencies strongly filter the cross channel",
        ),
        check(
            "VAL4895_18_local_cross_envelope",
            suppression["largest_filtered_cross_channel_envelope"] < 1.0e-69,
            "filtered cross-only two-insertion envelope is recorded",
        ),
        check(
            "VAL4895_19_filter_scope",
            all(
                "not_total_clock_or_waveform_bound" in row["scope"]
                for row in suppression["rows"]
            ),
            "cross filtering is not promoted to a total waveform bound",
        ),
        check(
            "VAL4895_20_local_clauses",
            local["passed"]
            and len(local["clauses"]) == 8
            and local["closed_clauses"] == 8,
            "stationary decoupling theorem carries all eight clauses",
        ),
        check(
            "VAL4895_21_local_zero",
            local["zero_induced_force_norm"] == 0.0
            and local["zero_quadratic_stress_norm"] == 0.0
            and local["zero_collective_bath_displacement"] == 0.0,
            "induced force displacement and quadratic stress vanish at phi=theta=0",
        ),
        check(
            "VAL4895_22_local_GR_values",
            local["PPN_gamma"] == 1.0
            and local["PPN_beta"] == 1.0
            and "8 pi" in local["Newton_constant"],
            "selected stationary Newton and PPN values retained",
        ),
        check(
            "VAL4895_23_requirements",
            len(arbitration["requirements"]) == 8
            and arbitration["closed_requirements"] == 5,
            "five of eight reciprocal-parent requirements close",
        ),
        check(
            "VAL4895_24_open_FLRW",
            not requirement_lookup["covariant_bath_stress_owner"]["closed"]
            and not requirement_lookup["full_matrix_nonlocal_FLRW_background"][
                "closed"
            ]
            and not requirement_lookup["full_matrix_finite_k_constraints"][
                "closed"
            ],
            "nonstationary stress background and finite-k tests remain open",
        ),
        check(
            "VAL4895_25_old_closure_demoted",
            arbitration["current_local_cosmology_closure_status"]
            == "REMAINS_DEMOTED_AND_MUST_NOT_BE_REUSED",
            "old local Markov cosmology remains demoted",
        ),
        check(
            "VAL4895_26_no_retirement",
            arbitration["bath_cosmology_retirement_status"].startswith(
                "NOT_TRIGGERED"
            )
            and "POSITIVE_RECIPROCAL_PARENT_EXISTS"
            in arbitration["bath_cosmology_retirement_status"],
            "positive reciprocal candidate avoids premature route retirement",
        ),
        check(
            "VAL4895_27_cutoff_nonprediction",
            arbitration["cutoff_prediction_status"]
            == "FDT_CEILING_BENCHMARK_NOT_PARENT_SELECTED",
            "cutoff ceiling is not promoted to a prediction",
        ),
        check(
            "VAL4895_28_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "full_positive_homogeneous_spectral_parent_and_stationary_local_decoupling_derived_full_matrix_FLRW_stress_constraints_open_private_nonclaim",
            "L-737 unique private nonclaim status",
        ),
        check(
            "VAL4895_29_variables",
            len(new_variables) == 8
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "eight checkpoint variables are unique",
        ),
        check(
            "VAL4895_30_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4895_31_documents",
            "MTS_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_GATE_4895"
            in checkpoint
            and "PPC4161_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_4895"
            in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4895_32_registers",
            "1.188 Full reciprocal spectral parent" in equations
            and "139. A positive spectral matrix" in redteam
            and "PPC4161 checkpoint 4895" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4895_33_resume",
            "PPC4161_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_4895" in resume
            and NEXT_TARGET in resume,
            "resume and 4896 handoff updated",
        ),
        check(
            "VAL4895_34_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4895_35_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4895_36_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4895_37_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4895_full_spectral_matrix_local_decoupling.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4895_full_spectral_matrix_local_decoupling_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4895_38_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4895_39_next",
            NEXT_TARGET in checkpoint and arbitration["next_target"] == NEXT_TARGET,
            "4896 full-matrix FLRW stress target selected",
        ),
        check(
            "VAL4895_40_arbitration",
            arbitration["passed"] and calculation["all_checks_pass"],
            "4895 arbitration internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4895_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_GATE_4895_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4895_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4895_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4895_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4895_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4895_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
