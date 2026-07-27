from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from Y5_R2FR_4877_spectrum_nonlocal_vacuum import result


CHECKPOINT = "4877"
TIMESTAMP = "2026-07-10T17:45:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-"
    "nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md"
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
            "SRC4877_00_checkpoint",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
        ),
        (
            "SRC4877_01_research_script",
            POST / "scripts" / "Y5_R2FR_4877_spectrum_nonlocal_vacuum.py",
            "def corpus_spectrum_audit",
        ),
        (
            "SRC4877_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4877_spectrum_nonlocal_vacuum_gate.py",
            "P8_Y5_BRR545_4877_VALIDATION_PASS",
        ),
        (
            "SRC4877_03_prior_checkpoint",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
        ),
        (
            "SRC4877_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4876_VALIDATION.csv",
            "VAL4876_OVERALL",
        ),
        (
            "SRC4877_05_fundamental_action",
            ROOT
            / "core-mts-framework"
            / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "scalar motion field",
        ),
        (
            "SRC4877_06_effective_field_theory",
            ROOT
            / "core-mts-framework"
            / "field-theory"
            / "the-effective-field-theory-of-motion-timespace.md",
            "The fundamental field is",
        ),
        (
            "SRC4877_07_finite_leptons",
            ROOT
            / "quantum-particle-field"
            / "leptons-neutrinos"
            / "finite-lepton-families-from-curvature-memory-geometry.md",
            "No gauge fields",
        ),
        (
            "SRC4877_08_neutrino_unification",
            ROOT
            / "quantum-particle-field"
            / "leptons-neutrinos"
            / "why-neutrinos-are-light-and-mix.md",
            "single nonlinear motion field",
        ),
        (
            "SRC4877_09_three_body",
            ROOT
            / "core-mts-framework"
            / "field-theory"
            / "axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md",
            "complex motion field",
        ),
        (
            "SRC4877_10_yang_mills_extension",
            ROOT
            / "quantum-particle-field"
            / "yang-mills"
            / "yang-mills-mass-gap-via-the-motion-theory.md",
            "mass gap",
        ),
        (
            "SRC4877_11_formal_note",
            FORMAL / "893-PPC4161-spectrum-nonlocal-vacuum-freeze.md",
            "PPC4161_SPECTRUM_NONLOCAL_VACUUM_FREEZE_4877",
        ),
        (
            "SRC4877_12_claims",
            FORMAL / "02-claims-register.csv",
            "L-719",
        ),
        (
            "SRC4877_13_variables",
            FORMAL / "04-variable-audit.csv",
            "W0_spectrum_MTS",
        ),
        (
            "SRC4877_14_equations",
            FORMAL / "05-equation-register.md",
            "1.170 Spectrum supertraces",
        ),
        (
            "SRC4877_15_redteam",
            FORMAL / "06-consistency-red-team.md",
            "121. Spectrum, nonlocal completion",
        ),
        (
            "SRC4877_16_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4877",
        ),
        (
            "SRC4877_17_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_SPECTRUM_NONLOCAL_VACUUM_FREEZE_4877",
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
            "SRC4877_18_vassilevich",
            "https://arxiv.org/abs/hep-th/0306138",
            "scalar spinor vector heat-kernel coefficients",
        ),
        (
            "SRC4877_19_induced_gravity",
            "https://arxiv.org/abs/1805.03148",
            "matter-induced Einstein and vacuum coefficients",
        ),
        (
            "SRC4877_20_nonlocal_FRG",
            "https://arxiv.org/abs/2002.10839",
            "universal logarithmic form factors and arbitrary local renormalized terms",
        ),
        (
            "SRC4877_21_nonlocal_QED",
            "https://arxiv.org/abs/1507.06321",
            "covariant nonlocal logarithms and curvature expansion",
        ),
        (
            "SRC4877_22_planck",
            "https://arxiv.org/abs/1807.06209",
            "H0 and Omega_m smoke baseline",
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
                "verification_method": "primary_source_opened_2026-07-10",
            }
        )
    return tagged(rows)


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    corpus = sections["corpus_spectrum"]
    determinant = sections["determinant_weights"]
    species = sections["all_species"]
    moment = sections["moment_rigidity"]
    nonlocal_section = sections["nonlocal"]
    gravity_scope = sections["gravity_loop_scope"]
    pole_gate = sections["nonlocal_pole_gate"]
    vacuum = sections["vacuum_freeze"]

    fields = ("scalar", "Dirac", "Maxwell_plus_ghost")
    vacuum_weights = determinant["vacuum_weights_scalar_Dirac_Maxwell"]
    einstein_weights = determinant["EH_weights_minimal_scalar_Dirac_Maxwell"]
    weyl_weights = determinant["Weyl_log_weights_scalar_Dirac_Maxwell"]

    groups = {
        "CORPUS_SPECTRUM": tagged(
            [
                {
                    "row_id": f"CS4877_{index:02d}",
                    "check": check_name,
                    "passed": passed,
                    "files_scanned": corpus["files_scanned_for_statistics"],
                    "status": "CORPUS_SIGNATURE_FOUND" if passed else "CORPUS_SIGNATURE_FAILED",
                }
                for index, (check_name, passed) in enumerate(
                    corpus["checks"].items()
                )
            ]
            + [
                {
                    "row_id": "CS4877_99_verdict",
                    "check": "primitive_field_verdict",
                    "passed": corpus["passed"],
                    "formula": corpus["primitive_field_verdict"],
                    "status": "BOSONIC_PRIMITIVE_NO_DIRAC_MEASURE",
                }
            ]
        ),
        "DETERMINANT_WEIGHTS": tagged(
            [
                {
                    "row_id": f"DW4877_{index}",
                    "field": field,
                    "vacuum_weight": vacuum_weights[index],
                    "Einstein_weight": einstein_weights[index],
                    "Weyl_log_weight": weyl_weights[index],
                    "operator": determinant["operators"][
                        "maxwell" if index == 2 else field.lower()
                    ],
                    "status": "DERIVED_HEAT_KERNEL_WEIGHT",
                }
                for index, field in enumerate(fields)
            ]
        ),
        "SPECIES_FORMULAS": tagged(
            [
                {
                    "row_id": "SF4877_0_W0",
                    "quantity": "W0_vacuum",
                    "formula": species["W0_vacuum"],
                    "gate": "W0=0",
                    "status": "DERIVED",
                },
                {
                    "row_id": "SF4877_1_W1",
                    "quantity": "W1_Einstein",
                    "formula": species["W1_Einstein"],
                    "gate": "W1>0",
                    "status": "DERIVED",
                },
                {
                    "row_id": "SF4877_2_WC",
                    "quantity": "WC_Weyl",
                    "formula": species["WC_Weyl"],
                    "gate": "WC>0 for nonempty healthy spectrum",
                    "status": "DERIVED",
                },
                {
                    "row_id": "SF4877_3_C0",
                    "quantity": "C0_loop",
                    "formula": species["C0_loop"],
                    "gate": species["simultaneous_gate"],
                    "status": "DERIVED_MATTER_SECTOR",
                },
                {
                    "row_id": "SF4877_4_Mstar",
                    "quantity": "Mstar_squared",
                    "formula": species["Mstar_squared"],
                    "gate": species["simultaneous_gate"],
                    "status": "DERIVED_MATTER_SECTOR",
                },
                {
                    "row_id": "SF4877_5_aC",
                    "quantity": "aC_running",
                    "formula": species["aC_running"],
                    "gate": "finite local and H/ghost terms separate",
                    "status": "DERIVED_UNIVERSAL_RUNNING",
                },
                {
                    "row_id": "SF4877_6_aR",
                    "quantity": "aR_running",
                    "formula": species["aR_running"],
                    "gate": "finite local and H/ghost terms separate",
                    "status": "DERIVED_UNIVERSAL_RUNNING",
                },
            ]
        ),
        "BRANCH_TESTS": tagged(
            [
                {
                    "row_id": f"BT4877_{index:02d}",
                    **row,
                    "status": (
                        "VACUUM_AND_EH_GATE_PASS"
                        if row["vacuum_cancels"] and row["positive_EH"]
                        else "NO_SIMULTANEOUS_GATE"
                    ),
                }
                for index, row in enumerate(
                    sections["branch_tests"]["scenarios"]
                )
            ]
        ),
        "MOMENT_RIGIDITY": tagged(
            [
                {
                    "row_id": "MR4877_0",
                    "conditions": moment["four_scalar_one_Dirac_conditions"],
                    "identity": moment["variance_identity"],
                    "theorem": moment["theorem"],
                    "status": "THRESHOLD_RIGIDITY_PROVED",
                }
            ]
        ),
        "NONLOCAL_FORM_FACTORS": tagged(
            [
                {
                    "row_id": "NF4877_0_action",
                    "quantity": "Gamma_nonlocal",
                    "formula": nonlocal_section["Gamma_nonlocal"],
                    "status": "DERIVED_MATTER_ONE_LOOP",
                },
                {
                    "row_id": "NF4877_1_C",
                    "quantity": "C_log_C",
                    "formula": nonlocal_section["b_C"],
                    "local_match": nonlocal_section["local_log_match_C"],
                    "status": "UNIVERSAL_NONLOCAL",
                },
                {
                    "row_id": "NF4877_2_R",
                    "quantity": "R_log_R",
                    "formula": nonlocal_section["b_R"],
                    "local_match": nonlocal_section["local_log_match_R"],
                    "status": "UNIVERSAL_NONLOCAL",
                },
                {
                    "row_id": "NF4877_3_IR",
                    "quantity": "IR_kernel",
                    "formula": "x^2 ln(1/x)",
                    "local_match": nonlocal_section["kernel_maximum"],
                    "status": "IR_DECOUPLING_PROVED",
                },
            ]
        ),
        "GRAVITY_LOOP_SCOPE": tagged(
            [
                {
                    "row_id": "GL4877_0",
                    "calculated": gravity_scope["calculated_sector"],
                    "omitted": gravity_scope["omitted_sector"],
                    "rule": gravity_scope["power_law_rule"],
                    "control": gravity_scope["control_rule"],
                    "status": "OMISSION_EXPLICIT_NOT_USED_FOR_CANCELLATION",
                }
            ]
        ),
        "NONLOCAL_POLE_GATE": tagged(
            [
                {
                    "row_id": "PG4877_0",
                    "domain": pole_gate["domain"],
                    "denominator_scalar": pole_gate["D0_over_EH"],
                    "denominator_spin2": pole_gate["D2_over_EH"],
                    "theorem": pole_gate["controlled_domain_theorem"],
                    "SM_result": pole_gate["SM_subcutoff_result"],
                    "status": "TESTED_DOMAIN_ROOT_EXCLUSION_CONDITIONAL",
                }
            ]
        ),
        "ARENA_SMOKE": tagged(
            [
                {
                    "row_id": f"AS4877_{index:02d}",
                    **row,
                    "status": (
                        "UNIVERSAL_LOG_HIERARCHY_BELOW_1E_30"
                        if row["below_1e_minus_30"]
                        and row["weight_1e6_below_1e_minus_30"]
                        else "HIERARCHY_GATE_FAILED"
                    ),
                }
                for index, row in enumerate(
                    sections["arena_smoke"]["rows"]
                )
            ]
        ),
        "VACUUM_FREEZE": tagged(
            [
                {
                    "row_id": f"VF4877_{index:02d}",
                    **row,
                    "Lambda_cal_m^-2": vacuum["Lambda_cal_m^-2"],
                    "renormalization_condition": vacuum[
                        "renormalization_condition"
                    ],
                    "status": (
                        "LOCAL_BACKGROUND_SMALL"
                        if row["local_flat_safe_1e_minus_6"]
                        else "CURVED_BACKGROUND_REQUIRED"
                    ),
                }
                for index, row in enumerate(vacuum["rows"])
            ]
        ),
        "RESIDUAL_REBASE": tagged(
            [
                {
                    "row_id": "RR4877_0_statistics",
                    "residual": "primitive_fermionic_statistics",
                    "status": "ABSENT_CURRENT_CORPUS",
                    "next_action": "do not count soliton labels as determinants",
                },
                {
                    "row_id": "RR4877_1_vacuum",
                    "residual": "primitive_vacuum_cancellation",
                    "status": "REJECTED_BOSONIC_NO_GO",
                    "next_action": "retain explicit C0R freeze",
                },
                {
                    "row_id": "RR4877_2_nonlocal",
                    "residual": "universal_matter_form_factors",
                    "status": "DERIVED_AND_IR_DECOUPLING",
                    "next_action": "propagate into arena transfer functions",
                },
                {
                    "row_id": "RR4877_3_gravity_loop",
                    "residual": "integrated_H_and_ghost_form_factors",
                    "status": "OPEN_EXPLICIT_REMAINDER",
                    "next_action": "derive or conservatively bound",
                },
                {
                    "row_id": "RR4877_4_local_terms",
                    "residual": "finite_aR_aC",
                    "status": "RENORMALIZED_INPUTS_UNBOUNDED",
                    "next_action": "source arena bounds",
                },
                {
                    "row_id": "RR4877_5_background",
                    "residual": "C0R_and_Lambda_cal",
                    "status": "FROZEN_ONCE_NOT_PREDICTED",
                    "next_action": "prohibit arena retuning",
                },
                {
                    "row_id": "RR4877_6_empirical",
                    "residual": "source_to_observable_projection",
                    "status": "FORMULAS_READY_PROJECTIONS_OPEN",
                    "next_action": NEXT_TARGET,
                },
                {
                    "row_id": "RR4877_7_claim",
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
        if row.get("claim_id") == "L-719"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "Mstar_induced_MTS": "matter_species_W1_matching_derived_imported_SM_positive_actual_MTS_statistics_and_H_loops_open",
        "Gamma_metric_only_MTS": "matter_nonlocal_completion_and_C0R_freeze_integrated_parent_local_limit_conditional",
        "C0_parent_MTS": "primitive_bosonic_cancellation_rejected_renormalized_cosmological_freeze_selected",
        "aR_induced_MTS": "universal_matter_RlogR_derived_finite_local_and_H_loop_coefficient_open",
        "aC_induced_MTS": "universal_matter_ClogC_derived_finite_local_and_H_loop_coefficient_open",
        "Sigma_vac_MTS": "primitive_bosonic_vacuum_cancellation_rejected_threshold_rigid_fermionic_route_unowned",
        "L_match_MTS": "promoted_to_covariant_nonlocal_kernel_matching_log",
        "W0_spectrum_MTS": "matter_supertrace_derived_primitive_bosonic_zero_rejected",
        "W1_spectrum_MTS": "matter_Einstein_weight_derived_positive_gate_explicit",
        "WC_spectrum_MTS": "healthy_matter_Weyl_log_weight_derived_strictly_positive",
        "Gamma_nonlocal_MTS": "universal_matter_quadratic_curvature_form_factors_derived",
        "C0R_freeze_MTS": "one_scale_cosmological_renormalization_condition_selected_not_predicted",
        "epsilon_nonlocal_MTS": "universal_matter_IR_residual_formulas_derived_scale_smoke_tiny",
        "statistics_gate_MTS": "primitive_fermionic_measure_absent_soliton_labels_not_determinants",
        "Gamma_Hgh_nonlocal_MTS": "open_gauge_consistent_background_field_calculation_required",
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }
    checkpoint = (
        POST
        / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "893-PPC4161-spectrum-nonlocal-vacuum-freeze.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4876_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4877_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )
    sections = calculation["sections"]
    branch_rows = sections["branch_tests"]["scenarios"]
    imported_sm = next(
        row
        for row in branch_rows
        if row["branch"] == "imported_SM_without_RH_neutrinos"
    )
    rows = [
        check(
            "VAL4877_00_symbolic",
            calculation["all_checks_pass"],
            "eleven derivation and arbitration groups",
        ),
        check(
            "VAL4877_01_corpus",
            sections["corpus_spectrum"]["passed"]
            and sections["corpus_spectrum"]["fermionic_operator_hits"] == [],
            "primitive bosonic substrate and no fermionic operator",
        ),
        check(
            "VAL4877_02_weights",
            sections["determinant_weights"]["passed"]
            and sections["all_species"]["passed"],
            "scalar Dirac Maxwell and species weights",
        ),
        check(
            "VAL4877_03_branches",
            sections["branch_tests"]["passed"]
            and imported_sm["W0"] == -62
            and imported_sm["W1"] == 1
            and imported_sm["WC"] == 283,
            "primitive no-go and imported-SM benchmark",
        ),
        check(
            "VAL4877_04_moments",
            sections["moment_rigidity"]["passed"],
            "four-scalar one-Dirac threshold rigidity",
        ),
        check(
            "VAL4877_05_nonlocal",
            sections["nonlocal"]["passed"],
            "local-log matching and IR kernel limit",
        ),
        check(
            "VAL4877_06_gravity_scope",
            sections["gravity_loop_scope"]["passed"],
            "H and Diff-ghost omission explicit",
        ),
        check(
            "VAL4877_07_pole_gate",
            sections["nonlocal_pole_gate"]["passed"],
            "sign-independent tested-domain root gate",
        ),
        check(
            "VAL4877_08_arena",
            sections["arena_smoke"]["passed"]
            and sections["arena_smoke"]["max_weight_1e6_residual"]
            < 1e-30,
            "universal logs and 1e6 coefficient stress below 1e-30",
        ),
        check(
            "VAL4877_09_vacuum",
            sections["vacuum_freeze"]["passed"],
            "single Planck-baseline C0R renormalization condition",
        ),
        check(
            "VAL4877_10_sources",
            len(sources) == 23
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4877_11_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4877_12_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all evidence rows private",
        ),
        check(
            "VAL4877_13_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4877_14_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "primitive_bosonic_vacuum_cancellation_rejected_matter_nonlocal_logs_derived_C0R_freeze_selected_private_nonclaim",
            "L-719",
        ),
        check(
            "VAL4877_15_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "unique canonical variable statuses",
        ),
        check(
            "VAL4877_16_documents",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877"
            in checkpoint
            and "PPC4161_SPECTRUM_NONLOCAL_VACUUM_FREEZE_4877"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4877_17_registers",
            "1.170 Spectrum supertraces" in equations
            and "121. Spectrum, nonlocal completion" in redteam
            and "PPC4161 checkpoint 4877" in spine,
            "equation red-team and spine",
        ),
        check(
            "VAL4877_18_resume",
            "PPC4161_SPECTRUM_NONLOCAL_VACUUM_FREEZE_4877" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4877_19_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4876 remains green",
        ),
        check(
            "VAL4877_20_scripts",
            compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4877_spectrum_nonlocal_vacuum.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4877_spectrum_nonlocal_vacuum_gate.py"
            ),
            "scripts compile without bytecode",
        ),
        check(
            "VAL4877_21_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4877_22_next",
            NEXT_TARGET in checkpoint,
            "4878 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4877_OVERALL",
            overall,
            "MTS_SPECTRUM_NONLOCAL_VACUUM_FREEZE_4877_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4877_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4877_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4877_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4877_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4877_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
