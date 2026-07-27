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

import Y5_R2FR_4894_nonlocal_spectral_consistency as research  # noqa: E402


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
            "SRC4894_06_checkpoint",
            POST
            / "4894-Y5-R2FR-parent-nonlocal-bath-kernel-self-consistent-Einstein-Boltzmann-or-cosmology-source-demotion-gate.md",
            "MTS_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_GATE_4894",
        ),
        (
            "SRC4894_07_formal",
            FORMAL
            / "910-PPC4161-nonlocal-spectral-completion-and-cosmology-demotion.md",
            "PPC4161_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_4894",
        ),
        (
            "SRC4894_08_claim",
            FORMAL / "02-claims-register.csv",
            "L-736",
        ),
        (
            "SRC4894_09_variables",
            FORMAL / "04-variable-audit.csv",
            "CosmoSource4894_MTS",
        ),
        (
            "SRC4894_10_equations",
            FORMAL / "05-equation-register.md",
            "1.187 Causal nonlocal kernel",
        ),
        (
            "SRC4894_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "138. A causal auto kernel",
        ),
        (
            "SRC4894_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4894",
        ),
        (
            "SRC4894_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_4894",
        ),
        (
            "SRC4894_14_research",
            SCRIPTS / "Y5_R2FR_4894_nonlocal_spectral_consistency.py",
            "def kernel_and_sum_rules",
        ),
        (
            "SRC4894_15_gate",
            SCRIPTS / "Y5_R2FR_4894_nonlocal_spectral_consistency_gate.py",
            "VAL4894_OVERALL",
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
    kernel = sections["kernel"]
    background = sections["background"]
    audit = sections["audit"]
    return {
        "KERNEL_SUM_RULES": tagged(kernel["rows"]),
        "KERNEL_TRANSFORM_CHECKS": tagged(kernel["normalization_rows"]),
        "KERNEL_SUMMARY": tagged(
            [scalar_summary(kernel, {"rows", "normalization_rows"})]
        ),
        "ONE_SIDED_BACKGROUNDS": tagged(background["rows"]),
        "ONE_SIDED_BACKGROUND_EVOLUTION": tagged(
            background["background_rows"]
        ),
        "ONE_SIDED_BACKGROUND_SUMMARY": tagged(
            [
                scalar_summary(
                    background, {"rows", "background_rows", "runs"}
                )
            ]
        ),
        "COMPLETION_REQUIREMENTS": tagged(audit["requirements"]),
        "ARBITRATION": tagged([audit]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "next_target": audit["next_target"],
                    "local_stationary_correspondence_status": audit[
                        "local_stationary_correspondence_status"
                    ],
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
    kernel = sections["kernel"]
    background = sections["background"]
    audit = sections["audit"]
    kernel_lookup = {row["cutoff_per_efold"]: row for row in kernel["rows"]}
    background_lookup = {
        row["cutoff_per_efold"]: row for row in background["rows"]
    }
    requirements = {
        row["requirement"]: row for row in audit["requirements"]
    }
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4893_VALIDATION.csv")
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-736"
    ]
    variable_symbols = (
        "GammaKernel4894_MTS",
        "SpectralMatrix4894_MTS",
        "Cphi4894_MTS",
        "Ctheta4894_MTS",
        "qBath4894_MTS",
        "Markov4894_MTS",
        "NonlocalBg4894_MTS",
        "CosmoSource4894_MTS",
    )
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    new_variables = [row for row in variable_rows if row["symbol"] in variable_symbols]
    variable_counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in variable_symbols
    }
    source_paths_exist = True
    for row in new_variables:
        for source_path in row["source_files"].split(";"):
            source_paths_exist = source_paths_exist and (ROOT / source_path).exists()
    checkpoint = (
        POST
        / "4894-Y5-R2FR-parent-nonlocal-bath-kernel-self-consistent-Einstein-Boltzmann-or-cosmology-source-demotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "910-PPC4161-nonlocal-spectral-completion-and-cosmology-demotion.md"
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
        OUTPUT / "P8_Y5_R2FR_4894_SOURCE_REGISTER.csv",
        *[
            OUTPUT / f"P8_Y5_R2FR_4894_{name}.csv" for name in groups
        ],
    ]
    allowed = kernel_lookup[kernel["cutoff_limit"]]
    rows = [
        check(
            "VAL4894_00_prior",
            bool(prior_validation)
            and prior_validation[-1]["check_id"] == "VAL4893_OVERALL"
            and prior_validation[-1]["status"] == "PASS",
            "4893 validation inherited",
        ),
        check(
            "VAL4894_01_sources",
            sections["sources"]["passed"]
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            "all source files and markers exist",
        ),
        check(
            "VAL4894_02_kernel_rows",
            kernel["passed"] and len(kernel["rows"]) == 5,
            "five spectral sum-rule rows generated",
        ),
        check(
            "VAL4894_03_kernel_normalization",
            len(kernel["normalization_rows"]) == 12
            and max(
                row["absolute_transform_residual"]
                for row in kernel["normalization_rows"]
            )
            < 1.0e-9,
            "causal time kernel reproduces analytic frequency response",
        ),
        check(
            "VAL4894_04_cutoff",
            0.2516 < kernel["cutoff_limit"] < 0.2518,
            "exact FDT cutoff inherited",
        ),
        check(
            "VAL4894_05_Cphiphi",
            0.1258 < kernel["allowed_cutoff_C_phi_phi"] < 0.1260,
            "auto static susceptibility derived",
        ),
        check(
            "VAL4894_06_cross_q",
            2.38 < kernel["allowed_cutoff_q"] < 2.39,
            "rank-one cross amplitude derived",
        ),
        check(
            "VAL4894_07_Cthetatheta",
            0.7150
            < kernel["allowed_cutoff_minimum_C_theta_theta"]
            < 0.7152
            and kernel[
                "allowed_cutoff_minimum_C_theta_theta_over_3OmegaX"
            ]
            > 4.86,
            "compulsory reciprocal compression term is large",
        ),
        check(
            "VAL4894_08_positive_completion",
            abs(allowed["saturated_static_determinant"]) < 1.0e-14
            and kernel["completed_rank_one_spectral_eigenvalues_at_cutoff"][0]
            == 0.0
            and kernel["completed_rank_one_spectral_eigenvalues_at_cutoff"][1]
            > 0.8,
            "rank-one spectral completion is positive semidefinite",
        ),
        check(
            "VAL4894_09_current_determinant",
            -0.091
            < kernel[
                "current_parent_static_spectral_determinant_if_Ctheta_theta_zero"
            ]
            < -0.089,
            "zero reciprocal diagonal is not a positive common bath",
        ),
        check(
            "VAL4894_10_equal_coupling",
            abs(kernel["equal_coupling_cutoff"] - 0.6) < 1.0e-12
            and kernel["equal_coupling_cutoff"] > kernel["cutoff_limit"],
            "equal-coupling cutoff violates FDT ceiling",
        ),
        check(
            "VAL4894_11_Markov_conflict",
            0.0035
            < kernel["allowed_cutoff_friction_fraction_at_H0"]
            < 0.0036
            and allowed["local_Markov_fractional_error_at_omega_H0"] > 0.996,
            "allowed spectrum is non-Markovian at H0 frequency",
        ),
        check(
            "VAL4894_12_missing_parent_terms",
            not kernel["current_parent_has_reciprocal_theta_theta_kernel"]
            and not kernel["current_parent_has_diagonal_counterterm_rule"]
            and not kernel["current_parent_is_full_positive_spectral_matrix"],
            "current parent lacks reciprocal completion",
        ),
        check(
            "VAL4894_13_background_rows",
            background["passed"] and len(background["rows"]) == 3,
            "three one-sided nonlocal backgrounds reshot",
        ),
        check(
            "VAL4894_14_background_targets",
            all(
                row["shooting_residual_norm"] < 1.0e-8
                and abs(row["memory_today"] - 1.0e-3) < 1.0e-10
                and abs(row["clock_today"] - 0.049) < 1.0e-10
                and abs(row["E_today"] - 1.0) < 1.0e-9
                for row in background["rows"]
            ),
            "all one-sided backgrounds hit targets",
        ),
        check(
            "VAL4894_15_kappa_absorption",
            all(
                1.017 < row["kappa_ratio_to_local"] < 1.019
                for row in background["rows"]
            ),
            "background reshoot absorbs memory with about 1.8 percent kappa shift",
        ),
        check(
            "VAL4894_16_E_shift",
            all(
                6.4e-5
                < row["maximum_abs_fractional_E_shift_vs_local"]
                < 6.6e-5
                for row in background["rows"]
            ),
            "one-sided expansion shifts remain small after reshoot",
        ),
        check(
            "VAL4894_17_nonvariational_label",
            not background["variationally_complete"]
            and not background["usable_for_parent_prediction"]
            and "one_sided" in background["closure_label"],
            "background diagnostics are not promoted",
        ),
        check(
            "VAL4894_18_requirements",
            len(audit["requirements"]) == 8
            and audit["closed_requirements"] == 3,
            "three of eight nonlocal completion requirements close",
        ),
        check(
            "VAL4894_19_reciprocal_open",
            not requirements["reciprocal_theta_theta_kernel"]["closed"]
            and not requirements["diagonal_counterterm_rule"]["closed"]
            and not requirements[
                "covariant_bath_stress_in_Einstein_equations"
            ]["closed"],
            "reciprocal kernel counterterms and stress remain open",
        ),
        check(
            "VAL4894_20_no_fake_high_k",
            not requirements["nonlocal_high_k_constraint_system"]["closed"]
            and not audit["same_kernel_response_and_noise_compilable"],
            "known incomplete equations are not rerun as parent",
        ),
        check(
            "VAL4894_21_FDT_block",
            audit["FDT_covariance_status"]
            == "BLOCKED_BY_ABSENT_RECIPROCAL_KERNEL_COUNTERTERM_RULE_AND_BATH_STRESS",
            "same-kernel FDT covariance correctly blocked",
        ),
        check(
            "VAL4894_22_demotion",
            audit["current_cosmology_source_status"]
            == "DEMOTED_TO_PHENOMENOLOGICAL_CLOSURE_PENDING_FULL_2X2_KERNEL_COUNTERTERMS_AND_BATH_STRESS",
            "current bath cosmology source explicitly demoted",
        ),
        check(
            "VAL4894_23_local_correspondence",
            audit["local_stationary_correspondence_status"]
            == "UNCHANGED_THE_OBSTRUCTION_IS_IN_THE_COSMOLOGICAL_BATH_SOURCE",
            "stationary local correspondence retained",
        ),
        check(
            "VAL4894_24_claim",
            len(claims) == 1
            and claims[0]["status"]
            == "causal_auto_kernel_and_sum_rule_derived_current_bath_cosmology_demoted_to_phenomenological_closure_full_spectral_parent_open_private_nonclaim",
            "L-736 unique private nonclaim status",
        ),
        check(
            "VAL4894_25_variables",
            all(variable_counts[symbol] == 1 for symbol in variable_symbols),
            "eight checkpoint variables unique",
        ),
        check(
            "VAL4894_26_variable_sources",
            source_paths_exist,
            "all checkpoint variable source paths exist",
        ),
        check(
            "VAL4894_27_documents",
            "MTS_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_GATE_4894"
            in checkpoint
            and "PPC4161_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_4894"
            in formal_note,
            "checkpoint and formal markers",
        ),
        check(
            "VAL4894_28_registers",
            "1.187 Causal nonlocal kernel" in equations
            and "138. A causal auto kernel" in redteam
            and "PPC4161 checkpoint 4894" in spine,
            "equation red-team and spine registers updated",
        ),
        check(
            "VAL4894_29_resume",
            "PPC4161_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_4894" in resume
            and NEXT_TARGET in resume,
            "resume and 4895 handoff",
        ),
        check(
            "VAL4894_30_placeholders",
            not any(
                "MISSING_" in str(value)
                for row in all_rows
                for value in row.values()
            ),
            "no placeholder evidence rows",
        ),
        check(
            "VAL4894_31_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all generated evidence remains private nonclaim",
        ),
        check(
            "VAL4894_32_csv",
            all(path.exists() and read_csv(path) for path in output_paths),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4894_33_scripts",
            compile_source(
                SCRIPTS / "Y5_R2FR_4894_nonlocal_spectral_consistency.py"
            )
            and compile_source(
                SCRIPTS
                / "Y5_R2FR_4894_nonlocal_spectral_consistency_gate.py"
            ),
            "research and gate scripts compile",
        ),
        check(
            "VAL4894_34_pycache",
            not (SCRIPTS / "__pycache__").exists(),
            "no post-checkpoint script pycache",
        ),
        check(
            "VAL4894_35_next",
            NEXT_TARGET in checkpoint and audit["next_target"] == NEXT_TARGET,
            "4895 full-matrix or retirement target selected",
        ),
        check(
            "VAL4894_36_arbitration",
            audit["passed"] and calculation["all_checks_pass"],
            "4894 demotion arbitration internally passes",
        ),
    ]
    rows.append(
        check(
            "VAL4894_OVERALL",
            all(row["status"] == "PASS" for row in rows),
            "MTS_NONLOCAL_SPECTRAL_COMPLETION_DEMOTION_GATE_4894_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = research.result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4894_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4894_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4894_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4894_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4894_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
