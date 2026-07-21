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

import Y5_R2FR_4896_full_matrix_FLRW_stress as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
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


def scalar_summary(section: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in section.items() if key not in excluded}


def source_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in research.source_contract()["rows"]]
    outputs = [
        (
            "SRC4896_06_checkpoint",
            POST
            / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md",
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896",
        ),
        (
            "SRC4896_07_formal",
            FORMAL
            / "912-PPC4161-full-matrix-FLRW-stress-and-bath-cosmology-retirement.md",
            "PPC4161_FULL_MATRIX_FLRW_RETIREMENT_4896",
        ),
        (
            "SRC4896_08_claim",
            FORMAL / "02-claims-register.csv",
            "L-738",
        ),
        (
            "SRC4896_09_variables",
            FORMAL / "04-variable-audit.csv",
            "CosmoRoute4896_MTS",
        ),
        (
            "SRC4896_10_equations",
            FORMAL / "05-equation-register.md",
            "1.189 Covariant full-matrix FLRW stress",
        ),
        (
            "SRC4896_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "140. Conservation closure",
        ),
        (
            "SRC4896_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4896",
        ),
        (
            "SRC4896_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_FULL_MATRIX_FLRW_RETIREMENT_4896",
        ),
        (
            "SRC4896_14_research",
            SCRIPTS / "Y5_R2FR_4896_full_matrix_FLRW_stress.py",
            "def covariant_parent_and_stress",
        ),
        (
            "SRC4896_15_gate",
            SCRIPTS / "Y5_R2FR_4896_full_matrix_FLRW_stress_gate.py",
            "VAL4896_OVERALL",
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


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    parent = sections["parent"]
    uv = sections["uv"]
    quadrature = sections["quadrature"]
    shot = sections["shot"]
    diagnostics = sections["diagnostics"]
    evolution = sections["evolution"]
    scan = sections["scan"]
    convergence = sections["convergence"]
    arbitration = sections["arbitration"]
    return {
        "PARENT_STRESS_ROWS": tagged(parent["rows"]),
        "PARENT_STRESS_SUMMARY": tagged([scalar_summary(parent, {"rows"})]),
        "UV_CUTOFF_ROWS": tagged(uv["rows"]),
        "UV_SUMMARY": tagged([scalar_summary(uv, {"rows"})]),
        "QUADRATURE_SUMMARY": tagged(
            [
                scalar_summary(
                    quadrature, {"omega", "weights", "coupling"}
                )
            ]
        ),
        "RESHOT_SUMMARY": tagged([scalar_summary(shot, {"run"})]),
        "RESHOT_BACKGROUND_PARAMETERS": tagged(
            [
                {
                    "kappa": shot["run"]["kappa"],
                    "clock_scale": shot["run"]["clock_scale"],
                    "omega_lambda": shot["run"]["omega_lambda"],
                    "scalar_fraction_today": shot["run"][
                        "scalar_fraction_today"
                    ],
                    "bath_fraction_today": shot["run"][
                        "bath_fraction_today"
                    ],
                    "E_today": shot["run"]["E_today"],
                    "h_today": shot["run"]["h_today"],
                    "field_today": shot["run"]["field_today"],
                    "field_N_today": shot["run"]["field_n_today"],
                    "response_today": shot["run"]["response_today"],
                    "reciprocal_force_today": shot["run"][
                        "reciprocal_force_today"
                    ],
                }
            ]
        ),
        "CONSTRAINT_ROWS": tagged(diagnostics["rows"]),
        "CONSTRAINT_SUMMARY": tagged(
            [scalar_summary(diagnostics, {"rows"})]
        ),
        "BACKGROUND_EVOLUTION": tagged(evolution["rows"]),
        "BACKGROUND_SUMMARY": tagged([scalar_summary(evolution, {"rows"})]),
        "PARAMETER_SCAN": tagged(scan["rows"]),
        "PARAMETER_SCAN_SUMMARY": tagged([scalar_summary(scan, {"rows"})]),
        "CONVERGENCE_ROWS": tagged(convergence["rows"]),
        "CONVERGENCE_SUMMARY": tagged(
            [scalar_summary(convergence, {"rows"})]
        ),
        "COMPLETION_REQUIREMENTS": tagged(arbitration["requirements"]),
        "ARBITRATION": tagged(
            [scalar_summary(arbitration, {"requirements"})]
        ),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "stationary_local_GR_status": arbitration[
                        "stationary_local_GR_status"
                    ],
                    "metric_only_cosmology_status": arbitration[
                        "metric_only_cosmology_status"
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
    parent = sections["parent"]
    uv = sections["uv"]
    quadrature = sections["quadrature"]
    shot = sections["shot"]
    diagnostics = sections["diagnostics"]
    evolution = sections["evolution"]
    scan = sections["scan"]
    convergence = sections["convergence"]
    arbitration = sections["arbitration"]
    requirement_lookup = {
        row["requirement"]: row for row in arbitration["requirements"]
    }
    previous_validation = read_csv(
        OUTPUT / "P8_Y5_BRR545_4895_VALIDATION.csv"
    )
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-738"
    ]
    variable_symbols = (
        "gOmega4896_MTS",
        "bClock4896_MTS",
        "DClock4896_MTS",
        "rhoBath4896_MTS",
        "EFull4896_MTS",
        "MeffUV4896_MTS",
        "Shoot4896_MTS",
        "Scan4896_MTS",
        "CosmoRoute4896_MTS",
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
        / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "912-PPC4161-full-matrix-FLRW-stress-and-bath-cosmology-retirement.md"
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
        OUTPUT / "P8_Y5_R2FR_4896_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4896_{name}.csv" for name in groups
        ],
    ]
    evolution_lookup = {
        row["redshift"]: row for row in evolution["rows"]
    }
    rows = [
        check(
            "VAL4896_00_prior",
            bool(previous_validation)
            and previous_validation[-1]["check_id"] == "VAL4895_OVERALL"
            and previous_validation[-1]["status"] == "PASS",
            "4895 validation inherited",
        ),
        check(
            "VAL4896_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all prior and generated source markers exist",
        ),
        check(
            "VAL4896_02_parent_rows",
            parent["passed"] and len(parent["rows"]) == 6,
            "closed continuum stress parent contains six derived objects",
        ),
        check(
            "VAL4896_03_parent_owner",
            parent["stress_from_same_closed_parent"]
            and parent["clock_current_conserved"]
            and parent["counterterm_auxiliary_is_algebraic"],
            "response stress and clock current have one parent",
        ),
        check(
            "VAL4896_04_spectral_values",
            0.1258 < parent["C_phi_phi"] < 0.1260
            and 0.7150 < parent["C_theta_theta"] < 0.7152
            and 2.383 < parent["q_cross"] < 2.384,
            "4895 reciprocal coefficients inherited",
        ),
        check(
            "VAL4896_05_uv_ratio",
            2.0725
            < uv["effective_planck_ratio_at_FDT_ceiling"]
            < 2.0728,
            "exact early effective Planck ratio derived",
        ),
        check(
            "VAL4896_06_uv_H",
            0.6945 < uv["early_H_over_GR_at_FDT_ceiling"] < 0.6948
            and abs(uv["early_fractional_H_shift_at_FDT_ceiling"]) > 0.30,
            "minimum early expansion shift exceeds thirty percent",
        ),
        check(
            "VAL4896_07_cutoff_conflict",
            uv["all_FDT_allowed_cutoffs_fail"]
            and uv["minimum_cutoff_for_internal_gate"]
            > uv["FDT_cutoff_ceiling"]
            and uv["cutoff_gap_factor"] > 4.5,
            "ten-percent early gate and FDT ceiling do not overlap",
        ),
        check(
            "VAL4896_08_uv_rows",
            len(uv["rows"]) == 3
            and all(
                not row["passes_internal_ten_percent_gate"]
                for row in uv["rows"]
            ),
            "all sampled allowed cutoffs fail the early gate",
        ),
        check(
            "VAL4896_09_quadrature",
            quadrature["passed"]
            and abs(quadrature["relative_static_residual"]) < 1.0e-13
            and quadrature["mode_count"] == 40,
            "continuum quadrature reproduces static susceptibility",
        ),
        check(
            "VAL4896_10_closure_fit",
            shot["closure_fit_success"]
            and shot["bath_target_closed"]
            and shot["E0_target_closed"],
            "bath fraction and E0 reshoot close",
        ),
        check(
            "VAL4896_11_memory_rejection",
            not shot["memory_target_closed"]
            and not shot["joint_reshoot_closed"]
            and shot["memory_shortfall_factor"] > 1000.0,
            "memory target fails by more than three orders of magnitude",
        ),
        check(
            "VAL4896_12_reshot_values",
            abs(shot["run"]["bath_fraction_today"] - 0.049) < 1.0e-12
            and abs(shot["run"]["E_today"] - 1.0) < 1.0e-12
            and 9.2e-7
            < shot["run"]["scalar_fraction_today"]
            < 9.4e-7,
            "reshot numerical values recorded",
        ),
        check(
            "VAL4896_13_reshot_parameters",
            22.6 < shot["run"]["clock_scale"] < 22.8
            and 0.6848 < shot["run"]["omega_lambda"] < 0.6850
            and 4.7e5 < shot["run"]["kappa"] < 4.9e5,
            "clock lambda and inherited kappa are finite",
        ),
        check(
            "VAL4896_14_Friedmann_identity",
            diagnostics["passed"]
            and diagnostics["maximum_Friedmann_derivative_residual"]
            < 1.0e-14,
            "differentiated Friedmann identity closes",
        ),
        check(
            "VAL4896_15_Raychaudhuri_identity",
            diagnostics["maximum_Raychaudhuri_identity_residual"]
            < 1.0e-14,
            "Raychaudhuri source identity closes",
        ),
        check(
            "VAL4896_16_denominator",
            diagnostics["minimum_Friedmann_denominator"] > 2.0,
            "full background remains on a positive Friedmann branch",
        ),
        check(
            "VAL4896_17_background_rows",
            evolution["passed"] and len(evolution["rows"]) == 8,
            "eight full-matrix background epochs recorded",
        ),
        check(
            "VAL4896_18_counterterm_fraction",
            -1.073 < evolution["counterterm_fraction_exact"] < -1.072
            and all(
                abs(
                    row["counterterm_fraction"]
                    - evolution["counterterm_fraction_exact"]
                )
                < 1.0e-12
                for row in evolution["rows"]
            ),
            "order-one theta counterterm fraction is exact at every epoch",
        ),
        check(
            "VAL4896_19_early_history",
            0.69
            < evolution_lookup[1.0e6]["H_ratio_to_matched_GR"]
            < 0.71
            and evolution_lookup[1100.0]["H_ratio_to_matched_GR"] > 1.3
            and evolution_lookup[10.0]["H_ratio_to_matched_GR"] > 1.45,
            "full reshoot is not a late-only deformation",
        ),
        check(
            "VAL4896_20_bath_history",
            evolution_lookup[1.0e6]["bath_clock_fraction"] < -1.0
            and evolution_lookup[1100.0]["bath_clock_fraction"] > 0.48
            and evolution_lookup[10.0]["bath_clock_fraction"] > 0.59,
            "pre-late bath fraction is order one",
        ),
        check(
            "VAL4896_21_multiplier",
            all(row["multiplier_fraction"] > 0.0 for row in evolution["rows"]),
            "failure is not caused by a negative multiplier branch",
        ),
        check(
            "VAL4896_22_scan_rows",
            scan["passed"]
            and len(scan["rows"]) == 24
            and scan["successful_rows"] == 24,
            "all 24 positive-parameter smoke rows integrate",
        ),
        check(
            "VAL4896_23_scan_memory",
            scan["maximum_memory_fraction"] < 2.0e-5
            and scan["maximum_memory_fraction_among_bath_close_rows"]
            < 2.0e-6,
            "scan never approaches the memory target",
        ),
        check(
            "VAL4896_24_scan_joint",
            scan["joint_close_rows"] == 0
            and "not_global_fit" in scan["scan_scope"],
            "scan has no joint closure and is not overstated",
        ),
        check(
            "VAL4896_25_convergence",
            convergence["passed"]
            and convergence["maximum_abs_fractional_memory_quadrature_shift"]
            < 0.02
            and convergence["maximum_abs_initial_time_memory_shift"]
            < 1.0e-5,
            "quadrature and start-time robustness pass",
        ),
        check(
            "VAL4896_26_requirements",
            len(arbitration["requirements"]) == 7
            and arbitration["closed_requirements"] == 4,
            "four of seven full-matrix cosmology requirements close",
        ),
        check(
            "VAL4896_27_physical_failures",
            not requirement_lookup["target_memory_activation"]["closed"]
            and not requirement_lookup["early_standard_gravity_limit"][
                "closed"
            ]
            and not requirement_lookup["reuse_previous_CMB_growth_likelihoods"][
                "closed"
            ],
            "memory early limit and likelihood reuse remain rejected",
        ),
        check(
            "VAL4896_28_retirement",
            arbitration["bath_cosmology_status"]
            == "RETIRED_AS_ACTIVE_FUNDAMENTAL_COSMOLOGY_SOURCE_FOR_GAMMA1_SIGMA0P3_FDT_ALLOWED_DIAGONAL_SUBTRACTION",
            "selected bath cosmology is explicitly retired",
        ),
        check(
            "VAL4896_29_local_GR",
            arbitration["stationary_local_GR_status"]
            == "UNCHANGED_4895_DECOUPLING_THEOREM_REMAINS_VALID",
            "stationary local-GR theorem remains unchanged",
        ),
        check(
            "VAL4896_30_metric_baseline",
            arbitration["metric_only_cosmology_status"]
            == "RETAIN_AS_BASELINE_UNTIL_A_DIFFERENT_DERIVED_EXTENSION_CLOSES",
            "metric-only cosmology restored as baseline",
        ),
        check(
            "VAL4896_31_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "full_matrix_stress_and_constraints_derived_selected_bath_cosmology_retired_metric_only_baseline_and_stationary_local_GR_retained_private_nonclaim",
            "L-738 unique private nonclaim status",
        ),
        check(
            "VAL4896_32_variables",
            len(new_variables) == 9
            and all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "nine checkpoint variables are unique",
        ),
        check(
            "VAL4896_33_variable_sources",
            variable_sources_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4896_34_documents",
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896" in checkpoint
            and "PPC4161_FULL_MATRIX_FLRW_RETIREMENT_4896" in formal_note,
            "checkpoint and formal markers exist",
        ),
        check(
            "VAL4896_35_registers",
            "1.189 Covariant full-matrix FLRW stress" in equations
            and "140. Conservation closure" in redteam
            and "PPC4161 checkpoint 4896" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4896_36_resume",
            "PPC4161_FULL_MATRIX_FLRW_RETIREMENT_4896" in resume
            and NEXT_TARGET in resume,
            "resume and 4897 handoff updated",
        ),
        check(
            "VAL4896_37_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4896_38_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4896_39_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4896_40_scripts",
            compile_source(SCRIPTS / "Y5_R2FR_4896_full_matrix_FLRW_stress.py")
            and compile_source(
                SCRIPTS / "Y5_R2FR_4896_full_matrix_FLRW_stress_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4896_41_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4896_42_next",
            NEXT_TARGET in checkpoint and arbitration["next_target"] == NEXT_TARGET,
            "4897 metric-only baseline and re-entry target selected",
        ),
        check(
            "VAL4896_43_arbitration",
            arbitration["passed"] and calculation["all_checks_pass"],
            "4896 retirement arbitration internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4896_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4896_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4896_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4896_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4896_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4896_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
