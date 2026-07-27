from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from Y5_R2FR_4876_integrated_H_matching import result


CHECKPOINT = "4876"
TIMESTAMP = "2026-07-11T03:00:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-"
    "nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row in rows
    ]


def source_rows() -> list[dict[str, Any]]:
    local = [
        (
            "SRC4876_00_checkpoint",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
        ),
        (
            "SRC4876_01_research_script",
            POST / "scripts" / "Y5_R2FR_4876_integrated_H_matching.py",
            "scalar_heat_kernel_matching",
        ),
        (
            "SRC4876_02_gate_script",
            POST / "scripts" / "Y5_R2FR_4876_integrated_H_matching_gate.py",
            "P8_Y5_BRR545_4876_VALIDATION_PASS",
        ),
        (
            "SRC4876_03_prior_checkpoint",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        (
            "SRC4876_04_prior_script",
            POST / "scripts" / "Y5_R2FR_4875_collective_metric_pole.py",
            "eh_projector_pole",
        ),
        (
            "SRC4876_05_open_parent_script",
            POST / "scripts" / "Y5_R2FR_4873_open_parent_induced_gravity.py",
            "induced_gravity_anchor",
        ),
        (
            "SRC4876_06_formal_note",
            FORMAL / "892-PPC4161-integrated-H-saddle-and-induced-coefficient-matching.md",
            "PPC4161_INTEGRATED_H_SADDLE_MATCHING_4876",
        ),
        (
            "SRC4876_07_claims",
            FORMAL / "02-claims-register.csv",
            "L-718",
        ),
        (
            "SRC4876_08_variables",
            FORMAL / "04-variable-audit.csv",
            "C0_parent_MTS",
        ),
        (
            "SRC4876_09_equations",
            FORMAL / "05-equation-register.md",
            "1.169 Integrated-H saddle",
        ),
        (
            "SRC4876_10_redteam",
            FORMAL / "06-consistency-red-team.md",
            "120. Integrated-H saddle",
        ),
        (
            "SRC4876_11_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4876",
        ),
        (
            "SRC4876_12_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_INTEGRATED_H_SADDLE_MATCHING_4876",
        ),
        (
            "SRC4876_13_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4875_VALIDATION.csv",
            "VAL4875_OVERALL",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local:
        text = path.read_text(encoding="utf-8", errors="replace")
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local",
                "source_path": str(path),
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": marker in text,
                "verification_method": "local_path_and_marker",
            }
        )
    web = [
        (
            "SRC4876_14_vassilevich",
            "https://arxiv.org/abs/hep-th/0306138",
            "heat-kernel a0/a2/a4 coefficients",
        ),
        (
            "SRC4876_15_sakharov",
            "https://arxiv.org/abs/1805.03148",
            "proper-time induced C0, GN and signed species weights",
        ),
        (
            "SRC4876_16_quadratic_gravity",
            "https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.104025",
            "quadratic-gravity scalar and spin-2 mass conventions",
        ),
    ]
    for source_id, url, use in web:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web_primary",
                "source_path": url,
                "source_exists": True,
                "marker": use,
                "marker_found": True,
                "verification_method": "primary_source_opened_2026-07-11",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    heat = sections["heat_kernel"]
    saddle = sections["parent_saddle"]
    regulator = sections["regulator_ward"]
    poles = sections["quadratic_poles"]
    newton = sections["newton_matching"]
    sum_rules = sections["vacuum_sum_rules"]

    groups = {
        "PARENT_ACTION": tagged(
            [
                {
                    "row_id": "PAR4876_0_action",
                    "quantity": "counterterm_complete_parent",
                    "formula": saddle["parent_action"],
                    "status": "DERIVED_PARENT_CONTRACT",
                },
                {
                    "row_id": "PAR4876_1_matching",
                    "quantity": "renormalized_coefficients",
                    "formula": saddle["renormalized_coefficients"],
                    "status": "DERIVED_MATCHING_IDENTITY",
                },
                {
                    "row_id": "PAR4876_2_saddle",
                    "quantity": "metric_equation",
                    "formula": saddle["saddle_equation"],
                    "status": "DERIVED_LOCAL_EQUATION",
                },
                {
                    "row_id": "PAR4876_3_flat_gate",
                    "quantity": "flat_saddle",
                    "formula": saddle["flat_saddle_gate"],
                    "status": "EXACT_GATE",
                },
            ]
        ),
        "HEAT_KERNEL_MATCHING": tagged(
            [
                {
                    "row_id": "HK4876_0_A2_raw",
                    "quantity": "A2_bulk_raw",
                    "formula": heat["A2_bulk_raw"],
                    "status": "DERIVED",
                },
                {
                    "row_id": "HK4876_1_A2_basis",
                    "quantity": "A2_bulk_4d_basis",
                    "formula": heat["A2_bulk_4d_basis"],
                    "status": "DERIVED_GAUSS_BONNET_REBASE",
                },
                {
                    "row_id": "HK4876_2_C0",
                    "quantity": "C0_loop",
                    "formula": heat["constant_loop"],
                    "status": "DERIVED_SCALAR_ANCHOR",
                },
                {
                    "row_id": "HK4876_3_Mstar",
                    "quantity": "Mstar_squared",
                    "formula": heat["Mstar_squared"],
                    "status": "DERIVED_SCALAR_ANCHOR",
                },
                {
                    "row_id": "HK4876_4_aR",
                    "quantity": "a_R_loop",
                    "formula": heat["a_R_loop"],
                    "status": "DERIVED_SCALAR_ANCHOR",
                },
                {
                    "row_id": "HK4876_5_aC",
                    "quantity": "a_C_loop",
                    "formula": heat["a_C_loop"],
                    "status": "DERIVED_SCALAR_ANCHOR",
                },
                {
                    "row_id": "HK4876_6_aE",
                    "quantity": "a_E_loop",
                    "formula": heat["a_E_loop"],
                    "status": "DERIVED_SCALAR_ANCHOR",
                },
            ]
        ),
        "SADDLE_GATE": tagged(
            [
                {
                    "row_id": "SG4876_0_general",
                    "quantity": "Lambda_bg",
                    "formula": saddle["maximally_symmetric_local_saddle"],
                    "status": "DERIVED",
                },
                {
                    "row_id": "SG4876_1_scalar",
                    "quantity": "Lambda_bg_scalar_only",
                    "formula": saddle["massless_scalar_only_lambda"],
                    "status": "NONZERO_CUTOFF_SCALE",
                },
                {
                    "row_id": "SG4876_2_no_go",
                    "quantity": "scalar_only_flatness",
                    "formula": saddle["scalar_only_flat_no_go"],
                    "status": "REJECT_NATURAL_FLAT_SCALAR_ONLY",
                },
                {
                    "row_id": "SG4876_3_SK",
                    "quantity": "SK_vacuum_response",
                    "formula": sections["sk_vacuum"]["metric_response_exact"],
                    "status": "NONZERO_RESPONSE_DERIVED",
                },
            ]
        ),
        "REGULATOR_WARD": tagged(
            [
                {
                    "row_id": "RW4876_0_regulator",
                    "quantity": "proper_time_regulator",
                    "formula": regulator["regulator"],
                    "status": "COVARIANT_SCALAR_REGULATOR",
                },
                {
                    "row_id": "RW4876_1_covariance",
                    "quantity": "operator_variation",
                    "formula": regulator["covariance"],
                    "status": "DERIVED",
                },
                {
                    "row_id": "RW4876_2_trace",
                    "quantity": "Ward_trace",
                    "formula": regulator["ward_step"],
                    "status": "ZERO_BY_CYCLICITY",
                },
                {
                    "row_id": "RW4876_3_scope",
                    "quantity": "full_parent_scope",
                    "formula": regulator["scope"],
                    "status": "H_MEASURE_EXTENSION_OPEN",
                },
            ]
        ),
        "QUADRATIC_POLES": tagged(
            [
                {
                    "row_id": "QP4876_0_m0",
                    "quantity": "m0_squared",
                    "formula": poles["m0_squared"],
                    "status": "DERIVED_SCALAR_ANCHOR",
                },
                {
                    "row_id": "QP4876_1_m2",
                    "quantity": "m2_squared",
                    "formula": poles["m2_squared"],
                    "status": "DERIVED_PROBLEMATIC_LOCAL_SPIN2_SCALE",
                },
                {
                    "row_id": "QP4876_2_epsilon0",
                    "quantity": "epsilon_scalar",
                    "formula": poles["epsilon_scalar"],
                    "status": "DERIVED_IR_GATE",
                },
                {
                    "row_id": "QP4876_3_epsilon2",
                    "quantity": "epsilon_spin2",
                    "formula": poles["epsilon_spin2"],
                    "status": "DERIVED_IR_GATE",
                },
                {
                    "row_id": "QP4876_4_residue",
                    "quantity": "spin2_residue_structure",
                    "formula": poles["partial_fraction"],
                    "status": "OPPOSITE_MASSIVE_RESIDUE",
                },
                {
                    "row_id": "QP4876_5_domain",
                    "quantity": "EFT_domain",
                    "formula": poles["IR_gate"],
                    "status": "CONDITIONAL_IR_ONLY",
                },
            ]
        ),
        "NEWTON_MATCHING": tagged(
            [
                {
                    "row_id": "NM4876_0_GN",
                    "quantity": "GN_relation",
                    "formula": newton["GN_relation"],
                    "status": "DERIVED_MATCHING_RELATION",
                },
                {
                    "row_id": "NM4876_1_combination",
                    "quantity": "measured_combination",
                    "formula": newton["measured_combination"],
                    "status": "ONE_COMBINATION_FIXED_NOT_PREDICTION",
                },
                *[
                    {
                        "row_id": f"NM4876_{index + 2}_sample",
                        "quantity": "Lambda_over_Mbar_Pl",
                        "N_s_times_h": sample["N_s_times_h"],
                        "value": sample["Lambda_over_Mbar_Pl"],
                        "status": "ALGEBRAIC_SCALE_SAMPLE",
                    }
                    for index, sample in enumerate(newton["samples"])
                ],
            ]
        ),
        "VACUUM_SUM_RULES": tagged(
            [
                {
                    "row_id": "VS4876_0_quartic",
                    "quantity": "quartic_weight",
                    "formula": sum_rules["quartic_weight"],
                    "target": "0",
                    "status": "SUM_RULE_DERIVED",
                },
                {
                    "row_id": "VS4876_1_quadratic",
                    "quantity": "quadratic_weight",
                    "formula": sum_rules["quadratic_weight"],
                    "target": "0",
                    "status": "SUM_RULE_DERIVED",
                },
                {
                    "row_id": "VS4876_2_logarithmic",
                    "quantity": "logarithmic_weight",
                    "formula": sum_rules["logarithmic_weight"],
                    "target": "0",
                    "status": "SUM_RULE_DERIVED",
                },
                {
                    "row_id": "VS4876_3_EH",
                    "quantity": "newton_weight",
                    "formula": sum_rules["newton_weight"],
                    "target": ">0",
                    "status": "POSITIVE_EH_GATE",
                },
                {
                    "row_id": "VS4876_4_example",
                    "quantity": "constructive_example",
                    "formula": sum_rules["constructive_example"],
                    "target": "0,0,0,positive",
                    "status": "COMPATIBILITY_PROOF_NOT_MTS_OWNERSHIP",
                },
            ]
        ),
        "IR_HIERARCHY_SMOKE": tagged(
            [
                {
                    "row_id": f"IR4876_{index:02d}",
                    **row,
                    "status": (
                        "EH_DOMINANT_BELOW_ONE_PERCENT"
                        if row["IR_dominant_at_1_percent"]
                        else "ONE_PERCENT_GATE_NOT_MET"
                    ),
                }
                for index, row in enumerate(
                    sections["hierarchy_samples"]["rows"]
                )
            ]
        ),
        "RESIDUAL_REBASE": tagged(
            [
                {
                    "row_id": "RR4876_0_parent",
                    "residual": "counterterm_complete_parent",
                    "status": "CLOSED_AT_ONE_LOOP_LOCAL_ORDER",
                    "next_action": "extend to full spectrum and nonlocal kernels",
                },
                {
                    "row_id": "RR4876_1_regulator",
                    "residual": "matter_regulator_Ward",
                    "status": "CLOSED_FOR_PUBLIC_METRIC_REAL_SCALAR",
                    "next_action": "extend to H measure and all species",
                },
                {
                    "row_id": "RR4876_2_saddle",
                    "residual": "scalar_only_flat_saddle",
                    "status": "REJECTED",
                    "next_action": "test signed MTS spectrum sum rules",
                },
                {
                    "row_id": "RR4876_3_vacuum",
                    "residual": "full_MTS_vacuum_selection",
                    "status": "CONSTRUCTIVE_ROUTE_OPEN",
                    "next_action": "calculate actual spectrum weights",
                },
                {
                    "row_id": "RR4876_4_poles",
                    "residual": "higher_curvature_poles",
                    "status": "SCALAR_ANCHOR_LOCATED_IR_GATE_DERIVED",
                    "next_action": "derive nonlocal denominators",
                },
                {
                    "row_id": "RR4876_5_GN",
                    "residual": "Newton_constant",
                    "status": "MICROSCOPIC_COMBINATION_MATCHED",
                    "next_action": "derive Ns xi LambdaUV independently",
                },
                {
                    "row_id": "RR4876_6_empirical",
                    "residual": "arena_specific_hierarchy",
                    "status": "FORMULA_READY_NOT_CALIBRATED",
                    "next_action": "map qmax after full matching",
                },
                {
                    "row_id": "RR4876_7_claim",
                    "residual": "local_GR_claim",
                    "status": "PRIVATE_NONCLAIM",
                    "next_action": NEXT_TARGET,
                },
            ]
        ),
    }
    return groups


def compile_source(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError:
        return False
    return True


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

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-718"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "Mstar_induced_MTS": "one_loop_massive_scalar_matching_and_GN_combination_derived_positive_spin2_IR_residue_conditional",
        "Gamma_metric_only_MTS": "counterterm_complete_integrated_parent_saddle_and_scalar_IR_hierarchy_derived_vacuum_selection_open",
        "Pi_spin2_MTS": "massless_spin2_IR_pole_retained_quadratic_pole_hierarchy_derived_private_nonclaim",
        "Z_H_parent_MTS": "counterterm_complete_integrated_Diff_parent_constructed_contour_and_full_spectrum_open",
        "BRST_H_MTS": "covariant_matter_proper_time_Ward_derived_full_H_measure_conditional",
        "P_BR_MTS": "EH_inversion_and_scalar_quadratic_extra_pole_locations_derived",
        "C0_parent_MTS": "scalar_loop_derived_scalar_only_flat_saddle_rejected_full_spectrum_open",
        "aR_induced_MTS": "scalar_one_loop_coefficient_and_extra_scalar_pole_derived",
        "aC_induced_MTS": "scalar_one_loop_coefficient_and_problematic_spin2_scale_derived",
        "Sigma_vac_MTS": "constructive_scalar_Dirac_cancellation_exists_actual_MTS_spectrum_open",
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }
    checkpoint = (
        POST
        / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "892-PPC4161-integrated-H-saddle-and-induced-coefficient-matching.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4875_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4876_{name}.csv" for name in groups
    ]
    all_rows = [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )
    rows = [
        check(
            "VAL4876_00_symbolic",
            calculation["all_checks_pass"],
            "eight derivation groups",
        ),
        check(
            "VAL4876_01_heat_kernel",
            calculation["sections"]["heat_kernel"]["passed"],
            "A2 basis and coefficients",
        ),
        check(
            "VAL4876_02_saddle",
            calculation["sections"]["parent_saddle"]["passed"],
            "scalar-only saddle no-go",
        ),
        check(
            "VAL4876_03_SK",
            calculation["sections"]["sk_vacuum"]["passed"],
            "SK vacuum response",
        ),
        check(
            "VAL4876_04_regulator",
            calculation["sections"]["regulator_ward"]["passed"],
            "covariant trace Ward identity",
        ),
        check(
            "VAL4876_05_poles",
            calculation["sections"]["quadratic_poles"]["passed"],
            "scalar and spin2 pole scales",
        ),
        check(
            "VAL4876_06_Newton",
            calculation["sections"]["newton_matching"]["passed"],
            "Newton matching combination",
        ),
        check(
            "VAL4876_07_sum_rules",
            calculation["sections"]["vacuum_sum_rules"]["passed"],
            "constructive signed spectrum",
        ),
        check(
            "VAL4876_08_hierarchy",
            calculation["sections"]["hierarchy_samples"][
                "all_deep_IR_rows_pass"
            ],
            "all q/Lambda<=1e-2 rows below one percent",
        ),
        check(
            "VAL4876_09_sources",
            len(sources) == 17
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4876_10_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4876_11_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all evidence rows private",
        ),
        check(
            "VAL4876_12_csv",
            all(path.exists() and len(read_csv(path)) > 0 for path in output_paths),
            "nine evidence CSVs parse",
        ),
        check(
            "VAL4876_13_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "normalized_parent_and_scalar_one_loop_coefficients_derived_scalar_only_flat_saddle_rejected_balanced_spectrum_route_open_private_nonclaim",
            "L-718",
        ),
        check(
            "VAL4876_14_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "unique canonical variable statuses",
        ),
        check(
            "VAL4876_15_documents",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876"
            in checkpoint
            and "PPC4161_INTEGRATED_H_SADDLE_MATCHING_4876" in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4876_16_registers",
            "1.169 Integrated-H saddle" in equations
            and "120. Integrated-H saddle" in redteam
            and "PPC4161 checkpoint 4876" in spine,
            "equation red-team and spine",
        ),
        check(
            "VAL4876_17_resume",
            "PPC4161_INTEGRATED_H_SADDLE_MATCHING_4876" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4876_18_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4875 remains green",
        ),
        check(
            "VAL4876_19_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4876_integrated_H_matching.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4876_integrated_H_matching_gate.py"
            ),
            "scripts compile without bytecode",
        ),
        check(
            "VAL4876_20_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4876_21_next",
            NEXT_TARGET in checkpoint,
            "4877 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4876_OVERALL",
            overall,
            "INTEGRATED_H_SADDLE_MATCHING_4876_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4876_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4876_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4876_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4876_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4876_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
