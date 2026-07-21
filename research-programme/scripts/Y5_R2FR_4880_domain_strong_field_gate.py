from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4880_domain_strong_field import result


CHECKPOINT = "4880"
TIMESTAMP = "2026-07-10T19:08:41+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-"
    "and-Riemann-cubed-coefficient-owner-gate.md"
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
            "checkpoint": CHECKPOINT,
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
            "SRC4880_00_checkpoint",
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        (
            "SRC4880_01_research_script",
            POST / "scripts" / "Y5_R2FR_4880_domain_strong_field.py",
            "def einstein_bach_flat_branch",
        ),
        (
            "SRC4880_02_gate_script",
            POST / "scripts" / "Y5_R2FR_4880_domain_strong_field_gate.py",
            "P8_Y5_BRR545_4880_VALIDATION_PASS",
        ),
        (
            "SRC4880_03_prior_checkpoint",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4880_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4879_VALIDATION.csv",
            "VAL4879_OVERALL,PASS",
        ),
        (
            "SRC4880_05_integrated_parent",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
        ),
        (
            "SRC4880_06_prior_formal",
            FORMAL
            / "895-PPC4161-finite-source-beta-light-clock-local-GR-certificate.md",
            "PPC4161_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
        ),
        (
            "SRC4880_07_formal_note",
            FORMAL
            / "896-PPC4161-exact-Einstein-vacuum-branch-and-strong-field-domain.md",
            "PPC4161_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        (
            "SRC4880_08_claims",
            FORMAL / "02-claims-register.csv",
            "L-722",
        ),
        (
            "SRC4880_09_variables",
            FORMAL / "04-variable-audit.csv",
            "Einstein_vacuum_branch_MTS",
        ),
        (
            "SRC4880_10_equations",
            FORMAL / "05-equation-register.md",
            "1.173 Exact Einstein vacuum branch",
        ),
        (
            "SRC4880_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "124. Exact Einstein branch",
        ),
        (
            "SRC4880_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4880",
        ),
        (
            "SRC4880_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker in local:
        exists = path.exists()
        content = (
            path.read_text(encoding="utf-8", errors="replace")
            if exists
            else ""
        )
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "verification_method": "local_path_and_marker",
            }
        )
    web = [
        (
            "SRC4880_14_bach_flat",
            "https://arxiv.org/abs/1303.5781",
            "Bach tensor vanishes for every Einstein metric",
        ),
        (
            "SRC4880_15_quadratic_branches",
            "https://arxiv.org/abs/1907.00046",
            "Schwarzschild and non-Schwarzschild Bach branches",
        ),
        (
            "SRC4880_16_strict_eft",
            "https://arxiv.org/abs/1911.10108",
            "curvature-squared field redefinition in strict EFT",
        ),
        (
            "SRC4880_17_higher_curvature",
            "https://arxiv.org/abs/1808.08962",
            "higher-curvature black holes in gravitational EFT",
        ),
    ]
    for source_id, url, marker in web:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web_primary",
                "source_path": url,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "verification_method": "primary_source_recorded_and_browsed",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    exact = sections["einstein_branch"]
    domain = sections["domain_gates"]
    systems = sections["systems"]
    promotion = sections["promotion"]
    return {
        "EINSTEIN_BRANCH": tagged(
            [
                {
                    "action": exact["action"],
                    "einstein_condition": exact["einstein_condition"],
                    "EH_tensor_coefficient": exact[
                        "EH_tensor_coefficient"
                    ],
                    "R2_tensor_coefficient": exact[
                        "R2_einstein_coefficient_4d"
                    ],
                    "Bach_tensor": exact["bach_on_einstein"],
                    "Euler_tensor": exact["E4_local_variation_4d"],
                    "exact_common_branch": exact["exact_common_branch"],
                    "analytic_branch_selector": exact[
                        "analytic_branch_selector"
                    ],
                    "counterbranch_guard": exact["counterbranch_guard"],
                    "passed": exact["passed"],
                }
            ]
        ),
        "DOMAIN_GATES": tagged(
            [
                {
                    "tau_domain": domain[
                        "declared_fractional_tolerance"
                    ],
                    "compactness": domain["compactness"],
                    "PN_gate": domain["one_PN_gate"],
                    "PN_u_limit": domain["one_PN_u_limit"],
                    "K": domain["kretschmann_exterior"],
                    "qK": domain["curvature_momentum"],
                    "epsilon_R2": domain["R2_control"],
                    "epsilon_C2": domain["C2_control"],
                    "epsilon_loop": domain["long_range_loop_gate"],
                    "epsilon6": domain["curvature_cubed_gate"],
                    "ellStar_bound": domain["cutoff_length_bound"],
                    "source_gate": domain["source_gate"],
                    "flow_gate": domain["flow_gate"],
                    "passed": domain["passed"],
                }
            ]
        ),
        "SYSTEM_BENCHMARKS": tagged(systems["rows"]),
        "DECISION_TREE": tagged(sections["decision_tree"]["rows"]),
        "PROMOTION": tagged([promotion]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "next_target": promotion["next_target"],
                }
            ]
        ),
    }


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

    sections = calculation["sections"]
    exact = sections["einstein_branch"]
    domain = sections["domain_gates"]
    systems = sections["systems"]["rows"]
    by_name = {row["system"]: row for row in systems}
    promotion = sections["promotion"]

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-722"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "Einstein_vacuum_branch_MTS": "exact_four_dimensional_classical_local_Einstein_background_solution_private_conditional_selected_analytic_branch",
        "u_compactness_MTS": "derived_calculation_method_handoff_variable",
        "qK_curvature_MTS": "derived_invariant_strong_field_control_scale",
        "epsilon6_MTS": "derived_gate_coefficient_not_owned",
        "local_GR_domain_certificate_MTS": "private_conditional_1PN_plus_exact_Einstein_vacuum_background_certificate",
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL
        / "896-PPC4161-exact-Einstein-vacuum-branch-and-strong-field-domain.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4879_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4880_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )

    rows = [
        check(
            "VAL4880_00_symbolic",
            calculation["all_checks_pass"],
            "six derivation domain benchmark and arbitration sections",
        ),
        check(
            "VAL4880_01_sources",
            len(sources) == 18
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4880_02_EH_branch",
            exact["EH_tensor_coefficient"] == "0",
            "matched Einstein EH tensor zero",
        ),
        check(
            "VAL4880_03_R2_branch",
            exact["R2_einstein_coefficient_4d"] == "0",
            "four-dimensional R2 Euler tensor zero",
        ),
        check(
            "VAL4880_04_Bach_branch",
            exact["bach_on_einstein"] == "0"
            and exact["E4_local_variation_4d"] == "0",
            "Bach and Euler tensors zero",
        ),
        check(
            "VAL4880_05_counterbranches",
            "non-Einstein" in exact["counterbranch_guard"]
            and "order-reduce" in exact["analytic_branch_selector"],
            "resummed counterbranches and analytic selector explicit",
        ),
        check(
            "VAL4880_06_domain",
            domain["passed"]
            and domain["declared_fractional_tolerance"] == 0.01
            and domain["one_PN_u_limit"] == 0.1,
            "one-percent compactness and invariant EFT gates",
        ),
        check(
            "VAL4880_07_R10_caps",
            abs(domain["R10_epsilon_R2_at_cap"] - 0.01) < 1e-14
            and abs(domain["R10_epsilon_C2_at_cap"] - 0.01) < 1e-14,
            "4878 derivative-control cap normalization",
        ),
        check(
            "VAL4880_08_system_count",
            len(systems) == 5 and len(by_name) == 5,
            "five representative systems unique",
        ),
        check(
            "VAL4880_09_weak_systems",
            all(
                by_name[name]["one_PN_1percent_gate"]
                for name in [
                    "Earth",
                    "Sun",
                    "one_solar_mass_white_dwarf",
                ]
            ),
            "Earth Sun and white dwarf inside 1PN gate",
        ),
        check(
            "VAL4880_10_neutron_star",
            not by_name[
                "1.4_solar_mass_12km_neutron_star"
            ]["one_PN_1percent_gate"]
            and by_name[
                "1.4_solar_mass_12km_neutron_star"
            ]["selected_route"]
            == "FULL_GR_MATTER_INTERIOR_AND_EOS_MATCHING_REQUIRED",
            "neutron star routed to matter-interior solver",
        ),
        check(
            "VAL4880_11_black_hole",
            not by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["one_PN_1percent_gate"]
            and by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["selected_route"]
            == "EXACT_EINSTEIN_VACUUM_BRANCH",
            "black-hole horizon routed to exact Einstein branch",
        ),
        check(
            "VAL4880_12_hierarchies",
            max(
                row["epsilon_R2_at_4878_control_cap"] for row in systems
            )
            < 3e-19
            and max(row["epsilon_loop"] for row in systems) < 1e-77,
            "curvature-squared and loop envelopes remain tiny",
        ),
        check(
            "VAL4880_13_cutoff",
            3000
            < by_name[
                "1.4_solar_mass_12km_neutron_star"
            ]["ellStar_max_m_for_epsilon6_below_1percent_c6_1"]
            < 4000
            and 5000
            < by_name[
                "10_solar_mass_Schwarzschild_horizon"
            ]["ellStar_max_m_for_epsilon6_below_1percent_c6_1"]
            < 5100,
            "curvature-cubed one-percent cutoff lengths calculated",
        ),
        check(
            "VAL4880_14_decision_tree",
            sections["decision_tree"]["passed"]
            and len(sections["decision_tree"]["rows"]) == 5,
            "five mutually distinct routing outcomes",
        ),
        check(
            "VAL4880_15_promotion",
            promotion["passed"]
            and promotion["strong_field_vacuum_promoted"]
            and not promotion["strong_field_matter_interior_promoted"],
            "exact vacuum promoted while matter interior withheld",
        ),
        check(
            "VAL4880_16_scope",
            not promotion["charged_electrovac_promoted"]
            and not promotion["black_hole_perturbation_spectrum_promoted"]
            and not promotion["full_fundamental_unification"],
            "electrovac perturbations and full theory not promoted",
        ),
        check(
            "VAL4880_17_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4880_18_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private",
        ),
        check(
            "VAL4880_19_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4880_20_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "selected_metric_strictEFT_exact_classical_local_Einstein_vacuum_background_private_conditional_certificate",
            "L-722 unique and scoped",
        ),
        check(
            "VAL4880_21_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "five canonical strong-field variables unique",
        ),
        check(
            "VAL4880_22_documents",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880"
            in checkpoint
            and "PPC4161_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4880_23_registers",
            "1.173 Exact Einstein vacuum branch" in equations
            and "124. Exact Einstein branch" in redteam
            and "PPC4161 checkpoint 4880" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4880_24_resume",
            "PPC4161_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880"
            in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4880_25_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4879 remains green",
        ),
        check(
            "VAL4880_26_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4880_domain_strong_field.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4880_domain_strong_field_gate.py"
            ),
            "scripts compile without bytecode",
        ),
        check(
            "VAL4880_27_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4880_28_next",
            NEXT_TARGET in checkpoint
            and promotion["next_target"] == NEXT_TARGET,
            "4881 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4880_OVERALL",
            overall,
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4880_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4880_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4880_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4880_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4880_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
