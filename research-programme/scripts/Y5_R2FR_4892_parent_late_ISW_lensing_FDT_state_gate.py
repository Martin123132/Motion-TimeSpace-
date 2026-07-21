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

import Y5_R2FR_4892_parent_late_ISW_lensing_FDT_state as research  # noqa: E402


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
            "SRC4892_07_checkpoint",
            POST
            / "4892-Y5-R2FR-parent-late-ISW-lensing-line-of-sight-and-FDT-state-realization-or-CMB-source-demotion-gate.md",
            "MTS_PARENT_LOS_KMS_STATE_GATE_4892",
        ),
        (
            "SRC4892_08_formal",
            FORMAL / "908-PPC4161-parent-LOS-KMS-state.md",
            "PPC4161_PARENT_LOS_KMS_STATE_4892",
        ),
        (
            "SRC4892_09_claim",
            FORMAL / "02-claims-register.csv",
            "L-734",
        ),
        (
            "SRC4892_10_variables",
            FORMAL / "04-variable-audit.csv",
            "CMBgate4892_MTS",
        ),
        (
            "SRC4892_11_equations",
            FORMAL / "05-equation-register.md",
            "1.185 Parent non-Limber line of sight",
        ),
        (
            "SRC4892_12_redteam",
            FORMAL / "06-consistency-red-team.md",
            "136. A non-Limber transfer",
        ),
        (
            "SRC4892_13_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4892",
        ),
        (
            "SRC4892_14_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_PARENT_LOS_KMS_STATE_4892",
        ),
        (
            "SRC4892_15_research_script",
            SCRIPTS / "Y5_R2FR_4892_parent_late_ISW_lensing_FDT_state.py",
            "def line_of_sight_projection",
        ),
        (
            "SRC4892_16_gate_script",
            SCRIPTS
            / "Y5_R2FR_4892_parent_late_ISW_lensing_FDT_state_gate.py",
            "VAL4892_OVERALL",
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
    grid = sections["response_grid"]
    normalization = sections["transfer_normalization"]
    line_of_sight = sections["line_of_sight"]
    bath = sections["bath_state"]
    grid_summary = {
        key: value
        for key, value in grid.items()
        if key not in {"rows", "k_nodes", "N_nodes", "values", "interpolator"}
    }
    los_summary = {
        key: value
        for key, value in line_of_sight.items()
        if key
        not in {
            "rows",
            "convergence_rows",
            "lens_reconstruction_rows",
            "limber_comparison_rows",
        }
    }
    bath_summary = {key: value for key, value in bath.items() if key != "rows"}
    arbitration = sections["arbitration"]
    return {
        "RESPONSE_GRID": tagged(grid["rows"]),
        "RESPONSE_GRID_SUMMARY": tagged([grid_summary]),
        "TRANSFER_NORMALIZATION": tagged(normalization["rows"]),
        "TRANSFER_NORMALIZATION_SUMMARY": tagged(
            [
                {
                    key: value
                    for key, value in normalization.items()
                    if key != "rows"
                }
            ]
        ),
        "LOS_SPECTRA": tagged(line_of_sight["rows"]),
        "LOS_CONVERGENCE": tagged(line_of_sight["convergence_rows"]),
        "LENS_SOURCE_RECONSTRUCTION": tagged(
            line_of_sight["lens_reconstruction_rows"]
        ),
        "LIMBER_COMPARISON": tagged(
            line_of_sight["limber_comparison_rows"]
        ),
        "LOS_SUMMARY": tagged([los_summary]),
        "BATH_SCAN": tagged(bath["rows"]),
        "BATH_SUMMARY": tagged([bath_summary]),
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
    grid = sections["response_grid"]
    normalization = sections["transfer_normalization"]
    line_of_sight = sections["line_of_sight"]
    bath = sections["bath_state"]
    arbitration = sections["arbitration"]
    los_lookup = {row["ell"]: row for row in line_of_sight["rows"]}
    requirements = {
        row["requirement"]: row for row in arbitration["requirements"]
    }
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-734"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in (
            "DeltaISW4892_MTS",
            "DeltaLens4892_MTS",
            "ClTT4892_MTS",
            "ClPP4892_MTS",
            "ClTP4892_MTS",
            "Jbath4892_MTS",
            "rhoKMS4892_MTS",
            "LambdaKMS4892_MTS",
            "CMBgate4892_MTS",
        )
    }
    checkpoint = (
        POST
        / "4892-Y5-R2FR-parent-late-ISW-lensing-line-of-sight-and-FDT-state-realization-or-CMB-source-demotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (FORMAL / "908-PPC4161-parent-LOS-KMS-state.md").read_text(
        encoding="utf-8"
    )
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
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4891_VALIDATION.csv")
    all_rows = sources + [row for rows in groups.values() for row in rows]
    output_paths = [
        OUTPUT / "P8_Y5_R2FR_4892_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4892_{name}.csv" for name in groups
        ],
    ]
    rows = [
        check(
            "VAL4892_00_prior",
            bool(prior_validation)
            and prior_validation[-1]["check_id"] == "VAL4891_OVERALL"
            and prior_validation[-1]["status"] == "PASS",
            "4891 validation inherited",
        ),
        check(
            "VAL4892_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all parent and generated source markers exist",
        ),
        check(
            "VAL4892_02_CAMB",
            sections["sources"]["CAMB_version"] == "1.6.6",
            "CAMB 1.6.6 locked",
        ),
        check(
            "VAL4892_03_response_grid",
            grid["passed"]
            and len(grid["rows"]) == 50
            and grid["minimum_k_h_per_Mpc"] == 1.0e-3
            and grid["maximum_k_h_per_Mpc"] == 1.0e-1,
            "validated five-by-ten parent response grid loaded",
        ),
        check(
            "VAL4892_04_transfer_sources",
            normalization["NumSources"] == 3
            and normalization["q_count"] == 1694,
            "CAMB temperature E and lens transfer sources present",
        ),
        check(
            "VAL4892_05_transfer_normalization",
            normalization["passed"]
            and normalization["maximum_abs_fractional_residual"] < 1.21e-3,
            "temperature and lens C_l normalization reconstructed",
        ),
        check(
            "VAL4892_06_ISW_identity",
            line_of_sight["temperature_source_identity"].startswith(
                "delta S_T^ISW=2"
            )
            and line_of_sight["Weyl_normalization"]
            == "W_CAMB=k^2 Phi_Weyl",
            "exact CAMB ISW identity mapped to parent Weyl response",
        ),
        check(
            "VAL4892_07_lens_identity",
            line_of_sight["lensing_source_identity"]
            == "delta S_phi=(R_W-1) S_phi_CAMB",
            "linear parent lens source identity fixed",
        ),
        check(
            "VAL4892_08_lens_reconstruction",
            line_of_sight["maximum_abs_lens_reconstruction_residual"]
            < 6.0e-4,
            "direct Bessel integration reconstructs CAMB lens transfer",
        ),
        check(
            "VAL4892_09_resolution",
            line_of_sight["maximum_abs_resolution_shift_difference"]
            < 5.0e-4,
            "1201-versus-2401 source projection convergence",
        ),
        check(
            "VAL4892_10_LOS_rows",
            line_of_sight["passed"]
            and len(line_of_sight["rows"]) == len(research.ELL_REPORT),
            "fourteen non-Limber angular rows calculated",
        ),
        check(
            "VAL4892_11_low_ell_TT",
            0.010 < los_lookup[2]["fractional_TT_shift"] < 0.011
            and 0.012 < los_lookup[4]["fractional_TT_shift"] < 0.013,
            "signed low-ell TT enhancement locked",
        ),
        check(
            "VAL4892_12_lensing_sign",
            all(
                row["fractional_lensing_potential_shift"] < 0.0
                for row in line_of_sight["rows"]
            )
            and -0.0126
            < los_lookup[10]["fractional_lensing_potential_shift"]
            < -0.0123,
            "signed lens-potential suppression locked",
        ),
        check(
            "VAL4892_13_cross_sign",
            all(
                row["fractional_T_phi_shift"] > 0.0
                for row in line_of_sight["rows"]
            ),
            "parent T-phi cross shift is positive on sampled multipoles",
        ),
        check(
            "VAL4892_14_cosmic_variance_scale",
            max(
                abs(row["TT_shift_over_cosmic_variance"])
                for row in line_of_sight["rows"]
                if row["ell"] <= 10
            )
            < 0.03,
            "low-ell TT shift remains below three percent of per-ell cosmic variance",
        ),
        check(
            "VAL4892_15_IR_coverage",
            los_lookup[2]["temperature_response_domain_power_fraction"]
            < 0.29
            and los_lookup[10]["temperature_response_domain_power_fraction"]
            > 0.93
            and line_of_sight["IR_temperature_incomplete_below_ell_10"],
            "infrared TT coverage gap is explicit",
        ),
        check(
            "VAL4892_16_high_k_coverage",
            los_lookup[200]["lensing_response_domain_power_fraction"] > 0.86
            and los_lookup[400]["lensing_response_domain_power_fraction"] < 0.57
            and line_of_sight["high_k_lensing_incomplete_above_ell_200"],
            "high-k lensing coverage gap is explicit",
        ),
        check(
            "VAL4892_17_Limber_crosscheck",
            len(line_of_sight["limber_comparison_rows"]) == 6
            and line_of_sight[
                "maximum_abs_Limber_non_Limber_shift_difference"
            ]
            < 9.0e-5,
            "independent Limber and non-Limber lens shifts agree",
        ),
        check(
            "VAL4892_18_bath_scan",
            bath["passed"] and len(bath["rows"]) == 4,
            "positive super-Drude KMS bath scan ran",
        ),
        check(
            "VAL4892_19_bath_candidate",
            0.0210 < bath["candidate_impulse_variance"] < 0.0211
            and bath["candidate_to_bound_ratio"] < 0.75
            and bath["candidate_positive_KMS_state_exists"],
            "explicit normalized KMS state lies below FDT bound",
        ),
        check(
            "VAL4892_20_vacuum_cutoff",
            0.4341
            < bath["vacuum_cutoff_limit_times_DeltaN"]
            < 0.4343,
            "zero-temperature cutoff boundary solved",
        ),
        check(
            "VAL4892_21_non_Markov",
            not bath["candidate_local_Markov_valid"]
            and not bath["broad_Markov_vacuum_allowed"],
            "admissible state requires nonlocal memory",
        ),
        check(
            "VAL4892_22_state_scope",
            bath["state_existence_closed"]
            and not bath[
                "parent_selects_cutoff_temperature_or_cell_measure"
            ]
            and not bath["physical_temperature_conversion_allowed"]
            and not bath["noise_likelihood_allowed"],
            "state existence closes without fabricating parent selection",
        ),
        check(
            "VAL4892_23_requirements",
            len(arbitration["requirements"]) == 10
            and arbitration["closed_requirements"] == 5,
            "five of ten promotion requirements closed",
        ),
        check(
            "VAL4892_24_open_response",
            not requirements["infrared_parent_Weyl_response"]["closed"]
            and not requirements["high_k_parent_Weyl_response"]["closed"],
            "both parent response tails remain open",
        ),
        check(
            "VAL4892_25_open_parent_state",
            not requirements["parent_bath_state_selection"]["closed"]
            and not requirements[
                "self_consistent_parent_Einstein_Boltzmann_run"
            ]["closed"],
            "parent state selection and compiled transfer remain open",
        ),
        check(
            "VAL4892_26_no_likelihood",
            not arbitration["CMB_likelihood_allowed"]
            and not line_of_sight["official_likelihood_allowed"]
            and not requirements["official_CMB_likelihood"]["closed"],
            "no CMB likelihood claim",
        ),
        check(
            "VAL4892_27_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "non_Limber_fixed_background_LOS_and_normalized_KMS_state_existence_derived_IR_high_k_parent_state_selection_and_likelihood_open_private_nonclaim",
            "L-734 unique private nonclaim status",
        ),
        check(
            "VAL4892_28_variables",
            all(
                variable_counts[symbol] == 1 and symbol in variables
                for symbol in variable_counts
            ),
            "nine checkpoint variables unique",
        ),
        check(
            "VAL4892_29_documents",
            "MTS_PARENT_LOS_KMS_STATE_GATE_4892" in checkpoint
            and "PPC4161_PARENT_LOS_KMS_STATE_4892" in formal_note,
            "checkpoint and formal markers",
        ),
        check(
            "VAL4892_30_registers",
            "1.185 Parent non-Limber line of sight" in equations
            and "136. A non-Limber transfer" in redteam
            and "PPC4161 checkpoint 4892" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4892_31_resume",
            "PPC4161_PARENT_LOS_KMS_STATE_4892" in resume
            and NEXT_TARGET in resume,
            "resume and 4893 handoff",
        ),
        check(
            "VAL4892_32_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4892_33_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4892_34_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4892_35_scripts",
            compile_source(
                SCRIPTS
                / "Y5_R2FR_4892_parent_late_ISW_lensing_FDT_state.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4892_parent_late_ISW_lensing_FDT_state_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4892_36_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4892_37_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4893 response-tail and parent-state target selected",
        ),
        check(
            "VAL4892_38_arbitration",
            arbitration["passed"] and calculation["all_checks_pass"],
            "4892 internal arbitration passes without promotion",
        ),
    ]
    rows.append(
        check(
            "VAL4892_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_PARENT_LOS_KMS_STATE_GATE_4892_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4892_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4892_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4892_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4892_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4892_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
