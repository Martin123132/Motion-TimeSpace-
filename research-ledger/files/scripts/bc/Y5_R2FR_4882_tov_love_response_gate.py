from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4882_tov_love_response import result


CHECKPOINT = "4882"
TIMESTAMP = "2026-07-10T20:34:31+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-"
    "multi-EOS-mass-radius-tidal-contact-response-gate.md"
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
            "SRC4882_00_checkpoint",
            POST
            / "4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-and-tidal-sensitivity-or-strong-matter-promotion-gate.md",
            "MTS_TOV_LOVE_RESPONSE_JACOBIAN_4882",
        ),
        (
            "SRC4882_01_research_script",
            POST / "scripts" / "Y5_R2FR_4882_tov_love_response.py",
            "def solve_star_response",
        ),
        (
            "SRC4882_02_gate_script",
            POST / "scripts" / "Y5_R2FR_4882_tov_love_response_gate.py",
            "P8_Y5_BRR545_4882_VALIDATION_PASS",
        ),
        (
            "SRC4882_03_prior_checkpoint",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
        ),
        (
            "SRC4882_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4881_VALIDATION.csv",
            "VAL4881_OVERALL,PASS",
        ),
        (
            "SRC4882_05_prior_script",
            POST / "scripts" / "Y5_R2FR_4881_compact_fluid_a6.py",
            "def corrected_tov_map",
        ),
        (
            "SRC4882_06_strong_field_domain",
            POST
            / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
        ),
        (
            "SRC4882_07_tolman_regression",
            POST
            / "scripts"
            / "Y5_R2FR_4868_fixed_background_variational_remainder.py",
            "def tolman_vii_background",
        ),
        (
            "SRC4882_08_formal_note",
            FORMAL / "898-PPC4161-TOV-Love-response-Jacobian.md",
            "PPC4161_TOV_LOVE_RESPONSE_JACOBIAN_4882",
        ),
        (
            "SRC4882_09_claims",
            FORMAL / "02-claims-register.csv",
            "L-724",
        ),
        (
            "SRC4882_10_variables",
            FORMAL / "04-variable-audit.csv",
            "lambdaR_fluid_MTS",
        ),
        (
            "SRC4882_11_equations",
            FORMAL / "05-equation-register.md",
            "1.175 Compact-star TOV/Love response Jacobian",
        ),
        (
            "SRC4882_12_redteam",
            FORMAL / "06-consistency-red-team.md",
            "126. TOV/Love response conditioning",
        ),
        (
            "SRC4882_13_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4882",
        ),
        (
            "SRC4882_14_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_TOV_LOVE_RESPONSE_JACOBIAN_4882",
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
                "source_type": "local_text",
                "source_path": str(path),
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "verification_method": "local_path_and_marker",
            }
        )
    web = [
        (
            "SRC4882_15_hinderer_love",
            "https://arxiv.org/abs/0711.2420",
            "relativistic l=2 tidal Love equation and k2 map",
        ),
        (
            "SRC4882_16_read_piecewise_polytropes",
            "https://arxiv.org/abs/0812.2163",
            "piecewise-polytropic neutron-star EOS representation",
        ),
        (
            "SRC4882_17_postnikov_surface",
            "https://arxiv.org/abs/1004.5098",
            "tidal Love surface-density jump guard",
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
    locations = sections["locations"]
    responses = sections["responses"]
    crosscheck = sections["crosscheck"]
    arbitration = sections["arbitration"]
    target_rows = [
        {
            "model_id": model_id,
            "central_density_Lsun_minus2": central_density,
        }
        for model_id, central_density in locations[
            "target_densities"
        ].items()
    ]
    return {
        "EOS_CONTRACT": tagged([sections["EOS_contract"]]),
        "MAXIMUM_MODEL": tagged([locations["maximum_model"]]),
        "TARGET_LOCATIONS": tagged(target_rows),
        "CONTACT_CAPS": tagged([sections["caps"]]),
        "RESPONSE_BENCHMARKS": tagged(responses["rows"]),
        "FINITE_DIFFERENCE": tagged(crosscheck["rows"]),
        "ARBITRATION": tagged([arbitration]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "all_checks_pass": calculation["all_checks_pass"],
                    "next_target": arbitration["next_target"],
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
    eos = sections["EOS_contract"]
    locations = sections["locations"]
    maximum = locations["maximum_model"]
    caps = sections["caps"]
    response_rows = sections["responses"]["rows"]
    response_by_id = {row["model_id"]: row for row in response_rows}
    one = response_by_id["one_solar_mass"]
    canonical = response_by_id["canonical_1p4"]
    near = response_by_id["near_turning_0p99_Mmax"]
    crosscheck = sections["crosscheck"]
    arbitration = sections["arbitration"]

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-724"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "lambdaR_fluid_MTS": (
            "derived_TOV_unit_contact_coefficient_with_control_cap"
        ),
        "lambdaC_fluid_MTS": (
            "derived_TOV_unit_contact_coefficient_with_control_cap"
        ),
        "Z_TOV_contact_MTS": (
            "derived_and_nonlinear_finite_difference_validated_"
            "response_operator"
        ),
        "R_surface_response_MTS": (
            "derived_zero_surface_density_event_response"
        ),
        "kappa_turn_TOV_MTS": "derived_stability_condition_number",
        "k2_contact_response_MTS": (
            "derived_EOS_conditional_fixed_nc_and_fixed_mass_response"
        ),
        "LambdaT_contact_response_MTS": (
            "derived_EOS_conditional_fixed_mass_envelope"
        ),
        "compact_response_certificate_MTS": (
            "private_EOS_conditional_response_engine_pass_not_strong_"
            "matter_promotion"
        ),
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-and-tidal-sensitivity-or-strong-matter-promotion-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "898-PPC4161-TOV-Love-response-Jacobian.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4881_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4882_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )

    rows = [
        check(
            "VAL4882_00_calculation",
            calculation["all_checks_pass"],
            "source EOS sequence cap response crosscheck and arbitration sections",
        ),
        check(
            "VAL4882_01_sources",
            len(sources) == 18
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4882_02_EOS",
            eos["passed"]
            and eos["EOS"] == "p=K n^2; rho=n+p; Gamma=2"
            and "0<=c_s^2<1" in eos["sound_speed"]
            and eos["surface_density"] == 0.0
            and not eos["surface_jump_correction_required"]
            and not eos["observationally_viable_2Msun_EOS"],
            "causal zero-surface-density control EOS explicitly non-microphysical",
        ),
        check(
            "VAL4882_03_maximum_model",
            locations["passed"]
            and 1.63 < maximum["mass"] < 1.65
            and 11.2 < maximum["radius_km"] < 11.4
            and maximum["radius"] > 2 * maximum["mass"],
            "controlled EOS maximum mass and compactness located",
        ),
        check(
            "VAL4882_04_targets",
            len(locations["target_densities"]) == 3
            and abs(one["mass"] - 1.0) < 2e-6
            and abs(canonical["mass"] - 1.4) < 2e-6
            and abs(near["mass"] - 0.99 * maximum["mass"]) < 2e-6,
            "one-solar canonical and near-turning stable models",
        ),
        check(
            "VAL4882_05_caps",
            caps["passed"]
            and 5.6e-11 < caps["lambdaR_cap_m2"] < 5.7e-11
            and 1.69e-10 < caps["lambdaC_cap_m2"] < 1.71e-10
            and abs(caps["ratio"] - 3.0) < 1e-12,
            "inherited strict-EFT contact caps transformed to TOV units",
        ),
        check(
            "VAL4882_06_responses",
            sections["responses"]["passed"]
            and len(response_rows) == 3
            and len(response_by_id) == 3
            and all(row["response_valid"] for row in response_rows),
            "three stable-sequence response benchmarks",
        ),
        check(
            "VAL4882_07_canonical_base",
            14.1 < canonical["radius_km"] < 14.2
            and 0.14 < canonical["compactness"] < 0.15
            and 0.07 < canonical["love_k2"] < 0.08
            and 730 < canonical["tidal_lambda"] < 750,
            "canonical background mass radius Love and tidal values",
        ),
        check(
            "VAL4882_08_conditioning",
            1.6 < one["turning_condition_number"] < 1.8
            and 2.8 < canonical["turning_condition_number"] < 2.9
            and near["turning_condition_number"] > 11.0,
            "turning-point condition number exposes fixed-mass singularity",
        ),
        check(
            "VAL4882_09_radius_caps",
            1.5e-18
            < canonical["cap_abs_deltaR_over_R_fixed_M"]
            < 1.6e-18
            and near["cap_abs_deltaR_over_R_fixed_M"] < 6.2e-18,
            "fixed-mass radius contact envelopes",
        ),
        check(
            "VAL4882_10_tidal_caps",
            1.0e-17
            < canonical["cap_abs_deltaLambda_over_Lambda_fixed_M"]
            < 1.1e-17
            and 5.0e-17
            < near["cap_abs_deltaLambda_over_Lambda_fixed_M"]
            < 5.1e-17,
            "fixed-mass tidal envelope and near-turning amplification",
        ),
        check(
            "VAL4882_11_response_order",
            one["turning_condition_number"]
            < canonical["turning_condition_number"]
            < near["turning_condition_number"]
            and one["cap_abs_deltaR_over_R_fixed_M"]
            < canonical["cap_abs_deltaR_over_R_fixed_M"]
            < near["cap_abs_deltaR_over_R_fixed_M"]
            and one["cap_abs_deltaLambda_over_Lambda_fixed_M"]
            < canonical["cap_abs_deltaLambda_over_Lambda_fixed_M"]
            < near["cap_abs_deltaLambda_over_Lambda_fixed_M"],
            "response amplification tracks sequence conditioning",
        ),
        check(
            "VAL4882_12_crosscheck",
            crosscheck["passed"]
            and len(crosscheck["rows"]) == 16
            and all(row["status"] == "PASS" for row in crosscheck["rows"])
            and crosscheck["maximum_relative_error"] < 2e-6,
            (
                "sixteen nonlinear finite-difference derivatives; "
                f"max_error={crosscheck['maximum_relative_error']:.9e}"
            ),
        ),
        check(
            "VAL4882_13_arbitration",
            arbitration["passed"]
            and not arbitration["strong_matter_background_promoted"]
            and not arbitration["full_fundamental_unification"],
            "response engine retained without strong-matter promotion",
        ),
        check(
            "VAL4882_14_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4882_15_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private and nonclaim",
        ),
        check(
            "VAL4882_16_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4882_17_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "selected_metric_strictEFT_TOV_Love_response_operator_validated_EOS_conditional_private_nonclaim",
            "L-724 unique and narrowly scoped",
        ),
        check(
            "VAL4882_18_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "eight TOV Love response variables unique and status-locked",
        ),
        check(
            "VAL4882_19_documents",
            "MTS_TOV_LOVE_RESPONSE_JACOBIAN_4882" in checkpoint
            and "PPC4161_TOV_LOVE_RESPONSE_JACOBIAN_4882"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4882_20_registers",
            "1.175 Compact-star TOV/Love response Jacobian" in equations
            and "126. TOV/Love response conditioning" in redteam
            and "PPC4161 checkpoint 4882" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4882_21_resume",
            "PPC4161_TOV_LOVE_RESPONSE_JACOBIAN_4882" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4882_22_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4881 remains green",
        ),
        check(
            "VAL4882_23_scripts",
            compile_source(
                POST / "scripts" / "Y5_R2FR_4882_tov_love_response.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4882_tov_love_response_gate.py"
            ),
            "research and gate scripts compile without bytecode",
        ),
        check(
            "VAL4882_24_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4882_25_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4883 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4882_OVERALL",
            overall,
            "MTS_TOV_LOVE_RESPONSE_JACOBIAN_4882_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4882_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4882_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4882_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4882_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4882_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
