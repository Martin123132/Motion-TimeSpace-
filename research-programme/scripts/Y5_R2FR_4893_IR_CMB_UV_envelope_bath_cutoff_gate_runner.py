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

import Y5_R2FR_4893_IR_CMB_UV_envelope_bath_cutoff_gate as research  # noqa: E402


TIMESTAMP = datetime.now(timezone.utc).isoformat()
NEXT_TARGET = research.NEXT_TARGET


def serializable(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
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
            "SRC4893_11_checkpoint",
            POST
            / "4893-Y5-R2FR-infrared-Weyl-response-full-CMB-transfer-and-parent-bath-cutoff-selection-or-CMB-likelihood-demotion-gate.md",
            "MTS_IR_CMB_UV_BATH_CUTOFF_GATE_4893",
        ),
        (
            "SRC4893_12_formal",
            FORMAL
            / "909-PPC4161-infrared-CMB-UV-envelope-and-bath-cutoff.md",
            "PPC4161_IR_CMB_UV_BATH_CUTOFF_4893",
        ),
        (
            "SRC4893_13_claim",
            FORMAL / "02-claims-register.csv",
            "L-735",
        ),
        (
            "SRC4893_14_variables",
            FORMAL / "04-variable-audit.csv",
            "CMBgate4893_MTS",
        ),
        (
            "SRC4893_15_equations",
            FORMAL / "05-equation-register.md",
            "1.186 Infrared response",
        ),
        (
            "SRC4893_16_redteam",
            FORMAL / "06-consistency-red-team.md",
            "137. Infrared closure",
        ),
        (
            "SRC4893_17_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4893",
        ),
        (
            "SRC4893_18_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_IR_CMB_UV_BATH_CUTOFF_4893",
        ),
        (
            "SRC4893_19_research",
            SCRIPTS
            / "Y5_R2FR_4893_IR_CMB_UV_envelope_bath_cutoff_gate.py",
            "def infrared_line_of_sight",
        ),
        (
            "SRC4893_20_gate_runner",
            SCRIPTS
            / "Y5_R2FR_4893_IR_CMB_UV_envelope_bath_cutoff_gate_runner.py",
            "VAL4893_OVERALL",
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
    return {
        key: value
        for key, value in section.items()
        if key not in excluded
    }


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    response = sections["certified_response"]
    line_of_sight = sections["IR_line_of_sight"]
    uv = sections["UV_envelope"]
    lens = sections["full_k_lensing"]
    bath = sections["bath_cutoff"]
    arbitration = sections["arbitration"]
    uv_summary = scalar_summary(
        uv,
        {
            "k_nodes",
            "N_nodes",
            "central",
            "lower",
            "upper",
            "interpolators",
            "asymptotic_central",
            "asymptotic_uncertainty",
        },
    )
    return {
        "CERTIFIED_RESPONSE": tagged(response["rows"]),
        "ZERO_MODE_RESPONSE": tagged(response["zero_mode_rows"]),
        "RESPONSE_SUMMARY": tagged(
            [
                scalar_summary(
                    response,
                    {
                        "rows",
                        "zero_mode_rows",
                        "k_nodes",
                        "N_nodes",
                        "values",
                        "interpolator",
                    },
                )
            ]
        ),
        "IR_LOS_SPECTRA": tagged(line_of_sight["rows"]),
        "IR_LOS_CONVERGENCE": tagged(line_of_sight["convergence_rows"]),
        "IR_COMPLETION_COMPARISON": tagged(line_of_sight["comparison_rows"]),
        "IR_LOS_SUMMARY": tagged(
            [
                scalar_summary(
                    line_of_sight,
                    {"rows", "convergence_rows", "comparison_rows"},
                )
            ]
        ),
        "UV_PROJECTED_RESPONSE": tagged(
            read_csv(OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_RESPONSE.csv")
        ),
        "UV_ENVELOPE_SUMMARY": tagged([uv_summary]),
        "FULL_K_LENSING": tagged(lens["rows"]),
        "FULL_K_LENSING_SUMMARY": tagged(
            [scalar_summary(lens, {"rows"})]
        ),
        "FDT_ADJOINT_RESPONSE": tagged(bath["rows"]),
        "FDT_ADJOINT_IMPULSES": tagged(bath["impulse_rows"]),
        "FDT_CUTOFF_SUMMARY": tagged(
            [scalar_summary(bath, {"rows", "impulse_rows"})]
        ),
        "CMB_REQUIREMENTS": tagged(arbitration["requirements"]),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "CMB_likelihood_allowed": arbitration[
                        "CMB_likelihood_allowed"
                    ],
                    "next_target": arbitration["next_target"],
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
    response = sections["certified_response"]
    line_of_sight = sections["IR_line_of_sight"]
    uv = sections["UV_envelope"]
    lens = sections["full_k_lensing"]
    bath = sections["bath_cutoff"]
    arbitration = sections["arbitration"]
    los_lookup = {row["ell"]: row for row in line_of_sight["rows"]}
    comparison_lookup = {
        row["ell"]: row for row in line_of_sight["comparison_rows"]
    }
    lens_lookup = {row["ell"]: row for row in lens["rows"]}
    requirements = {
        row["requirement"]: row for row in arbitration["requirements"]
    }
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4892_VALIDATION.csv")
    tail_summary = read_csv(
        OUTPUT / "P8_Y5_R2FR_4893_TAIL_SOLVER_SUMMARY.csv"
    )[0]
    projected_summary = read_csv(
        OUTPUT / "P8_Y5_R2FR_4893_PROJECTED_UV_SUMMARY.csv"
    )[0]
    adjoint_summary = read_csv(
        OUTPUT / "P8_Y5_R2FR_4893_FDT_ADJOINT_SUMMARY.csv"
    )[0]
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-735"
    ]
    variable_symbols = (
        "RIR4893_MTS",
        "ClTTIR4893_MTS",
        "UVconstraint4893_MTS",
        "RUVenv4893_MTS",
        "ClLensUV4893_MTS",
        "Gadj4893_MTS",
        "LambdaFDT4893_MTS",
        "rhoKMS4893_MTS",
        "BathScale4893_MTS",
        "CMBgate4893_MTS",
    )
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in variable_symbols
    }
    new_variables = [row for row in variable_rows if row["symbol"] in variable_symbols]
    checkpoint_path = (
        POST
        / "4893-Y5-R2FR-infrared-Weyl-response-full-CMB-transfer-and-parent-bath-cutoff-selection-or-CMB-likelihood-demotion-gate.md"
    )
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "909-PPC4161-infrared-CMB-UV-envelope-and-bath-cutoff.md"
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
        OUTPUT / "P8_Y5_R2FR_4893_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4893_{name}.csv" for name in groups
        ],
    ]
    source_paths_exist = True
    for row in new_variables:
        for source_path in row["source_files"].split(";"):
            resolved = ROOT / source_path
            source_paths_exist = source_paths_exist and resolved.exists()
    rows = [
        check(
            "VAL4893_00_prior",
            bool(prior_validation)
            and prior_validation[-1]["check_id"] == "VAL4892_OVERALL"
            and prior_validation[-1]["status"] == "PASS",
            "4892 validation inherited",
        ),
        check(
            "VAL4893_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all source files and markers exist",
        ),
        check(
            "VAL4893_02_tail_attempt_recorded",
            tail_summary["passed"].lower() == "false"
            and float(tail_summary["maximum_relative_momentum_residual"])
            > 0.9,
            "raw UV point attempt fails rather than being hidden",
        ),
        check(
            "VAL4893_03_IR_grid",
            response["passed"]
            and response["minimum_k_h_per_Mpc"] == 1.0e-5
            and response["maximum_k_h_per_Mpc"] == 0.1,
            "certified response spans CAMB infrared floor through 0.1 h/Mpc",
        ),
        check(
            "VAL4893_04_IR_limit",
            response["IR_limit_max_abs_response_residual"] < 1.6e-7,
            "finite k response converges to directly solved zero mode",
        ),
        check(
            "VAL4893_05_IR_constraint",
            response["IR_max_relative_momentum_residual"] < 2.9e-6,
            "infrared momentum constraint closes",
        ),
        check(
            "VAL4893_06_CAMB_IR_floor",
            line_of_sight["IR_gap_closed"]
            and line_of_sight["minimum_CAMB_k_h_per_Mpc"] > 1.0e-5,
            "no low-k response padding remains",
        ),
        check(
            "VAL4893_07_low_ell_coverage",
            line_of_sight["minimum_low_ell_temperature_power_coverage"]
            > 0.99999,
            "low-ell TT response covers more than 99.999 percent power",
        ),
        check(
            "VAL4893_08_TT_ell2",
            0.0107 < los_lookup[2]["fractional_TT_shift"] < 0.0110,
            "IR-complete ell-2 TT shift locked",
        ),
        check(
            "VAL4893_09_TT_ell4",
            0.0121 < los_lookup[4]["fractional_TT_shift"] < 0.0123,
            "IR-complete ell-4 TT shift locked",
        ),
        check(
            "VAL4893_10_IR_completion_change",
            5.5e-4
            < comparison_lookup[2]["IR_completion_TT_change"]
            < 5.8e-4,
            "ell-2 truncation correction is finite and measured",
        ),
        check(
            "VAL4893_11_LOS_signs",
            all(
                row["fractional_lensing_potential_shift"] < 0.0
                and row["fractional_T_phi_shift"] > 0.0
                for row in line_of_sight["rows"]
            ),
            "non-Limber lens and cross signs remain stable",
        ),
        check(
            "VAL4893_12_LOS_resolution",
            line_of_sight["maximum_resolution_shift_difference"] < 5.0e-4,
            "IR-complete transfer passes resolution halving",
        ),
        check(
            "VAL4893_13_projected_UV",
            projected_summary["passed"].lower() == "true"
            and projected_summary["UV_point_prediction_allowed"].lower()
            == "false"
            and projected_summary["UV_envelope_allowed"].lower() == "true",
            "UV point rejected and envelope retained",
        ),
        check(
            "VAL4893_14_UV_envelope_width",
            uv["passed"]
            and uv["maximum_finite_k_envelope_width"] < 1.22e-4,
            "raw versus projected Weyl split bounded",
        ),
        check(
            "VAL4893_15_UV_asymptotic",
            uv["maximum_asymptotic_uncertainty"] < 1.23e-4
            and not uv["point_prediction_allowed"],
            "asymptotic response remains an envelope",
        ),
        check(
            "VAL4893_16_full_k_lens",
            lens["passed"] and len(lens["rows"]) == 10,
            "ten full-k linear lensing envelope rows run",
        ),
        check(
            "VAL4893_17_lens_ell10",
            -0.0126
            < lens_lookup[10]["central_fractional_lensing_shift"]
            < -0.0124,
            "full-k L10 lens suppression locked",
        ),
        check(
            "VAL4893_18_lens_ell200",
            -0.0041
            < lens_lookup[200]["central_fractional_lensing_shift"]
            < -0.0038,
            "full-k L200 lens suppression locked",
        ),
        check(
            "VAL4893_19_lens_ell400",
            -0.0032
            < lens_lookup[400]["central_fractional_lensing_shift"]
            < -0.0029,
            "full-k L400 lens suppression locked",
        ),
        check(
            "VAL4893_20_lens_envelope",
            lens["maximum_lensing_shift_envelope_width"] < 3.7e-5
            and not lens["point_prediction_allowed"],
            "UV uncertainty has a narrow angular envelope",
        ),
        check(
            "VAL4893_21_adjoint_impulses",
            bath["maximum_impulse_relative_residual"] < 8.8e-6
            and float(adjoint_summary["maximum_impulse_absolute_residual"])
            < 1.0e-15,
            "adjoint kernel reproduces four forward impulses",
        ),
        check(
            "VAL4893_22_cutoff_limit",
            0.2516 < bath["today_cutoff_limit"] < 0.2518,
            "exact present FDT cutoff limit solved",
        ),
        check(
            "VAL4893_23_reject_4892_state",
            1.72 < bath["candidate_4892_variance_to_budget"] < 1.73
            and not bath["candidate_4892_survives"],
            "4892 Lambda=0.3 point rejected",
        ),
        check(
            "VAL4893_24_parent_scales",
            27.7 < bath["Lambda1_variance_to_budget"] < 27.9
            and 1148.0
            < bath["memory_scale_Lambda15_variance_to_budget"]
            < 1149.0
            and bath["carrier_mass_floor_over_H0"] > 1.0e15,
            "existing parent scales do not select an allowed cutoff",
        ),
        check(
            "VAL4893_25_parent_cutoff_open",
            not bath["parent_cutoff_selected"]
            and not bath["full_line_of_sight_noise_covariance_closed"],
            "cutoff ownership and two-time covariance remain open",
        ),
        check(
            "VAL4893_26_requirements",
            len(arbitration["requirements"]) == 10
            and arbitration["closed_requirements"] == 6,
            "six of ten requirements closed",
        ),
        check(
            "VAL4893_27_open_point_branch",
            not requirements["high_k_parent_point_response"]["closed"],
            "high-k point prediction remains rejected",
        ),
        check(
            "VAL4893_28_open_nonlocal_parent",
            not requirements[
                "self_consistent_parent_Einstein_Boltzmann_run"
            ]["closed"]
            and not requirements["parent_bath_cutoff_selection"]["closed"],
            "nonlocal parent and bath ownership remain open",
        ),
        check(
            "VAL4893_29_no_likelihood",
            not arbitration["CMB_likelihood_allowed"]
            and not requirements["official_CMB_likelihood"]["closed"],
            "no CMB likelihood promotion",
        ),
        check(
            "VAL4893_30_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "IR_response_and_low_ell_transfer_closed_UV_lensing_envelope_and_FDT_rejection_derived_nonlocal_parent_cutoff_likelihood_open_private_nonclaim",
            "L-735 unique private nonclaim status",
        ),
        check(
            "VAL4893_31_variables",
            all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "ten checkpoint variables unique",
        ),
        check(
            "VAL4893_32_variable_sources",
            source_paths_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4893_33_documents",
            "MTS_IR_CMB_UV_BATH_CUTOFF_GATE_4893" in checkpoint
            and "PPC4161_IR_CMB_UV_BATH_CUTOFF_4893" in formal_note,
            "checkpoint and formal markers",
        ),
        check(
            "VAL4893_34_registers",
            "1.186 Infrared response" in equations
            and "137. Infrared closure" in redteam
            and "PPC4161 checkpoint 4893" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4893_35_resume",
            "PPC4161_IR_CMB_UV_BATH_CUTOFF_4893" in resume
            and NEXT_TARGET in resume,
            "resume and 4894 handoff",
        ),
        check(
            "VAL4893_36_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4893_37_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4893_38_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4893_39_scripts",
            all(
                compile_source(SCRIPTS / name)
                for name in (
                    "Y5_R2FR_4893_response_tail_solver.py",
                    "Y5_R2FR_4893_constraint_projected_UV_solver.py",
                    "Y5_R2FR_4893_FDT_adjoint_filter.py",
                    "Y5_R2FR_4893_IR_CMB_UV_envelope_bath_cutoff_gate.py",
                    "Y5_R2FR_4893_IR_CMB_UV_envelope_bath_cutoff_gate_runner.py",
                )
            ),
            "five 4893 scripts compile",
        ),
        check(
            "VAL4893_40_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4893_41_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4894 nonlocal-kernel decisive target selected",
        ),
        check(
            "VAL4893_42_arbitration",
            arbitration["passed"] and calculation["all_checks_pass"],
            "4893 internal arbitration passes without claim promotion",
        ),
    ]
    rows.append(
        check(
            "VAL4893_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_IR_CMB_UV_BATH_CUTOFF_GATE_4893_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4893_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4893_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4893_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4893_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4893_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
