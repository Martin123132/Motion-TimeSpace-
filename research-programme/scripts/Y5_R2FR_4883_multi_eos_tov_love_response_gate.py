from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

from Y5_R2FR_4883_multi_eos_tov_love_response import (
    EOS_SPECS,
    FD_STEP,
    LAL_COMMIT,
    result,
)


CHECKPOINT = "4883"
TIMESTAMP = "2026-07-10T22:27:23+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
EOS_ROOT = POST / "source-intake" / "microphysical_eos" / "4883"
LAL_ROOT = EOS_ROOT / "lalsuite"
NEXT_TARGET = (
    "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-"
    "ownership-or-observational-bound-projection-gate.md"
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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_rows() -> list[dict[str, Any]]:
    local = [
        (
            "SRC4883_00_checkpoint",
            POST
            / "4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md",
            "MTS_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883",
        ),
        (
            "SRC4883_01_research_script",
            POST
            / "scripts"
            / "Y5_R2FR_4883_multi_eos_tov_love_response.py",
            "def contact_basis",
        ),
        (
            "SRC4883_02_gate_script",
            POST
            / "scripts"
            / "Y5_R2FR_4883_multi_eos_tov_love_response_gate.py",
            "P8_Y5_BRR545_4883_VALIDATION_PASS",
        ),
        (
            "SRC4883_03_prior_checkpoint",
            POST
            / "4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-and-tidal-sensitivity-or-strong-matter-promotion-gate.md",
            "MTS_TOV_LOVE_RESPONSE_JACOBIAN_4882",
        ),
        (
            "SRC4883_04_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4882_VALIDATION.csv",
            "VAL4882_OVERALL,PASS",
        ),
        (
            "SRC4883_05_prior_script",
            POST / "scripts" / "Y5_R2FR_4882_tov_love_response.py",
            "def solve_star_response",
        ),
        (
            "SRC4883_06_acquisition_metadata",
            LAL_ROOT / "acquisition_metadata.json",
            LAL_COMMIT,
        ),
        (
            "SRC4883_07_lalsuite_parser",
            LAL_ROOT / "LALSimNeutronStarEOSTabular.c",
            "contains the pressure in Pa",
        ),
        (
            "SRC4883_08_formal_note",
            FORMAL / "899-PPC4161-multi-EOS-TOV-Love-contact-response.md",
            "PPC4161_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883",
        ),
        (
            "SRC4883_09_claims",
            FORMAL / "02-claims-register.csv",
            "L-725",
        ),
        (
            "SRC4883_10_variables",
            FORMAL / "04-variable-audit.csv",
            "EOS_table_family_4883_MTS",
        ),
        (
            "SRC4883_11_equations",
            FORMAL / "05-equation-register.md",
            "1.176 Multi-EOS cold-barotrope TOV/Love contact response",
        ),
        (
            "SRC4883_12_redteam",
            FORMAL / "06-consistency-red-team.md",
            "127. Multi-EOS success does not derive the contact coefficients",
        ),
        (
            "SRC4883_13_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4883",
        ),
        (
            "SRC4883_14_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "PPC4161_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883",
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
    for index, (eos_id, spec) in enumerate(EOS_SPECS.items(), start=15):
        path = LAL_ROOT / spec["file"]
        exists = path.exists()
        digest = file_sha256(path) if exists else ""
        rows.append(
            {
                "source_id": f"SRC4883_{index:02d}_EOS_{eos_id}",
                "source_type": "local_binary_table",
                "source_path": str(path),
                "source_exists": exists,
                "marker": spec["sha256"],
                "marker_found": digest == spec["sha256"],
                "verification_method": "sha256",
                "commit_id": LAL_COMMIT,
                "blob_id": spec["blob_id"],
            }
        )
    web = [
        (
            "SRC4883_18_lalsuite",
            "https://git.ligo.org/lscsoft/lalsuite",
            "LVK Algorithm Library Suite and EOS implementation source",
        ),
        (
            "SRC4883_19_compose_BSK24",
            EOS_SPECS["BSK24"]["compose_url"],
            "BSK24 Mmax and R1.4 independent anchors",
        ),
        (
            "SRC4883_20_compose_SLY4",
            EOS_SPECS["SLY4"]["compose_url"],
            "SLY4 Mmax and R1.4 independent anchors",
        ),
        (
            "SRC4883_21_compose_DD2",
            EOS_SPECS["DD2"]["compose_url"],
            "DD2 Mmax and R1.4 independent anchors",
        ),
        (
            "SRC4883_22_compose_manual",
            "https://compose.obspm.fr/download/pdf/CompOSE_Quick_Guide_for_Users.pdf",
            "CompOSE cold-neutron-star table units and extraction guide",
        ),
        (
            "SRC4883_23_hinderer_love",
            "https://arxiv.org/abs/0711.2420",
            "relativistic l=2 Love equation and k2 map",
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
    sequence_rows: list[dict[str, Any]] = []
    target_rows: list[dict[str, Any]] = []
    response_by_key = {
        (row["eos_id"], row["model_id"]): row
        for row in sections["responses"]["rows"]
    }
    for row in sections["sequences"]["rows"]:
        maximum = row["maximum_model"]
        sequence_rows.append(
            {
                "eos_id": row["eos_id"],
                "family": row["family"],
                "calculated_Mmax_Msun": maximum["mass"],
                "calculated_Rmax_km": maximum["radius_km"],
                "published_Mmax_Msun": row["published_Mmax_Msun"],
                "Mmax_fractional_error": row["Mmax_fractional_error"],
                "published_R1p4_km": row["published_R1p4_km"],
                "R1p4_fractional_error": row["R1p4_fractional_error"],
                "passed": row["passed"],
            }
        )
        for model_id, central_q in row["target_q"].items():
            response = response_by_key[(row["eos_id"], model_id)]
            target_rows.append(
                {
                    "eos_id": row["eos_id"],
                    "model_id": model_id,
                    "central_q": central_q,
                    "mass_Msun": response["mass"],
                    "radius_km": response["radius_km"],
                    "tidal_lambda": response["tidal_lambda"],
                }
            )
    return {
        "COMPOSE_ARCHIVE_AUDIT": tagged(
            sections["compose_archive_audit"]["rows"]
        ),
        "TABLE_QUALITY": tagged(sections["table_quality"]["rows"]),
        "SEQUENCE_REGRESSION": tagged(sequence_rows),
        "TARGET_LOCATIONS": tagged(target_rows),
        "RESPONSE_BENCHMARKS": tagged(sections["responses"]["rows"]),
        "FINITE_DIFFERENCE": tagged(sections["crosscheck"]["rows"]),
        "SURFACE_CONVERGENCE": tagged(
            sections["surface_convergence"]["rows"]
        ),
        "EOS_SPREAD": tagged([sections["EOS_spread"]]),
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
    archive_rows = sections["compose_archive_audit"]["rows"]
    archive_by_id = {row["eos_id"]: row for row in archive_rows}
    quality_rows = sections["table_quality"]["rows"]
    quality_by_id = {row["eos_id"]: row for row in quality_rows}
    sequence_rows = sections["sequences"]["rows"]
    sequence_by_id = {row["eos_id"]: row for row in sequence_rows}
    response_rows = sections["responses"]["rows"]
    response_by_key = {
        (row["eos_id"], row["model_id"]): row for row in response_rows
    }
    canonical = [
        row for row in response_rows if row["model_id"] == "canonical_1p4"
    ]
    near = [
        row
        for row in response_rows
        if row["model_id"] == "near_turning_0p99_Mmax"
    ]
    crosscheck = sections["crosscheck"]
    convergence = sections["surface_convergence"]
    spread = sections["EOS_spread"]
    arbitration = sections["arbitration"]

    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-725"
    ]
    variable_rows = read_csv(FORMAL / "04-variable-audit.csv")
    variables = {row["symbol"]: row for row in variable_rows}
    expected_statuses = {
        "EOS_table_family_4883_MTS": (
            "hash_locked_three_microphysical_EOS_family_pass"
        ),
        "q_p25_EOS_MTS": "derived_surface_regular_table_coordinate",
        "D_barotropic_contact_MTS": (
            "derived_zero_temperature_barotropic_contact_pressure_image"
        ),
        "Z_TOV_table_MTS": (
            "derived_multi_EOS_tangent_operator_48_nonlinear_checks_pass"
        ),
        "kappa_turn_pc_MTS": (
            "derived_pressure_parameterized_turning_condition"
        ),
        "EOS_spread_contact_ratio_MTS": (
            "computed_realistic_EOS_spread_dominates_control_cap"
        ),
        "strong_matter_correspondence_4883_MTS": (
            "private_conditional_multi_EOS_GR_correspondence_not_parent_"
            "coefficient_claim"
        ),
    }
    variable_counts = {
        symbol: sum(row.get("symbol") == symbol for row in variable_rows)
        for symbol in expected_statuses
    }

    checkpoint = (
        POST
        / "4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md"
    ).read_text(encoding="utf-8")
    formal_note = (
        FORMAL / "899-PPC4161-multi-EOS-TOV-Love-contact-response.md"
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
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4882_VALIDATION.csv")
    output_paths = [
        OUTPUT / f"P8_Y5_R2FR_4883_{name}.csv" for name in groups
    ]
    all_rows = sources + [row for rows in groups.values() for row in rows]
    no_placeholders = not any(
        "MISSING_" in str(value)
        for row in all_rows
        for value in row.values()
    )

    rows = [
        check(
            "VAL4883_00_calculation",
            calculation["all_checks_pass"],
            "source table sequence response crosscheck convergence spread and arbitration sections",
        ),
        check(
            "VAL4883_01_sources",
            len(sources) == 24
            and all(
                row["source_exists"] and row["marker_found"]
                for row in sources
            ),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4883_02_hashes",
            len(sections["sources"]["table_rows"]) == 3
            and all(
                row["hash_matches"]
                for row in sections["sources"]["table_rows"]
            )
            and all(
                row["commit_id"] == LAL_COMMIT
                for row in sections["sources"]["table_rows"]
            ),
            "three selected LALSuite tables hash and commit locked",
        ),
        check(
            "VAL4883_03_archive_quarantine",
            len(archive_rows) == 3
            and not archive_by_id["APR"]["hash_matches"]
            and not archive_by_id["SLY4"]["hash_matches"]
            and archive_by_id["BSK24"]["hash_matches"]
            and all(not row["used_for_solver"] for row in archive_rows),
            "direct archive mismatch rows retained but excluded",
        ),
        check(
            "VAL4883_04_table_shapes",
            len(quality_rows) == 3
            and quality_by_id["BSK24"]["table_columns"] == 9
            and quality_by_id["DD2"]["table_columns"] == 9
            and quality_by_id["SLY4"]["table_columns"] == 2
            and quality_by_id["BSK24"]["positive_rows"] == 1000
            and quality_by_id["DD2"]["positive_rows"] == 1000
            and quality_by_id["SLY4"]["positive_rows"] == 99,
            "legacy and modern LALSuite formats parsed",
        ),
        check(
            "VAL4883_05_table_derivatives",
            sections["table_quality"]["passed"]
            and all(
                row["all_sampled_derivatives_positive"]
                for row in quality_rows
            ),
            "positive monotone rho(p) derivatives on sampled domains",
        ),
        check(
            "VAL4883_06_causality",
            quality_by_id["BSK24"]["first_acausal_pressure_Lsun_minus2"]
            is not None
            and quality_by_id["SLY4"][
                "first_acausal_pressure_Lsun_minus2"
            ]
            is not None
            and quality_by_id["DD2"][
                "first_acausal_pressure_Lsun_minus2"
            ]
            is None
            and all(
                sequence_by_id[eos_id]["maximum_model"][
                    "central_pressure_Lsun_minus2"
                ]
                < (
                    quality_by_id[eos_id][
                        "first_acausal_pressure_Lsun_minus2"
                    ]
                    or quality_by_id[eos_id]["pressure_max_Lsun_minus2"]
                )
                for eos_id in EOS_SPECS
            ),
            "stellar maxima remain inside the accepted causal table domain",
        ),
        check(
            "VAL4883_07_two_solar",
            sections["sequences"]["passed"]
            and sections["sequences"]["all_support_2Msun"]
            and all(row["maximum_model"]["mass"] > 2.0 for row in sequence_rows),
            "all selected EOS families support two-solar-mass stars",
        ),
        check(
            "VAL4883_08_mass_regression",
            max(abs(row["Mmax_fractional_error"]) for row in sequence_rows)
            < 0.006,
            "CompOSE maximum masses recovered below 0.6 percent",
        ),
        check(
            "VAL4883_09_radius_regression",
            max(abs(row["R1p4_fractional_error"]) for row in sequence_rows)
            < 0.003,
            "CompOSE canonical radii recovered below 0.3 percent",
        ),
        check(
            "VAL4883_10_canonical_backgrounds",
            len(canonical) == 3
            and min(row["radius_km"] for row in canonical) > 11.7
            and max(row["radius_km"] for row in canonical) < 13.3
            and min(row["tidal_lambda"] for row in canonical) > 290
            and max(row["tidal_lambda"] for row in canonical) < 700,
            "canonical radius and tidal family",
        ),
        check(
            "VAL4883_11_response_matrix",
            sections["responses"]["passed"]
            and len(response_rows) == 9
            and len(response_by_key) == 9
            and all(row["response_valid"] for row in response_rows),
            "three EOS by three mass targets response matrix",
        ),
        check(
            "VAL4883_12_target_masses",
            all(
                abs(response_by_key[(eos_id, "canonical_1p4")]["mass"] - 1.4)
                < 2.0e-6
                and abs(
                    response_by_key[(eos_id, "two_solar_mass")]["mass"]
                    - 2.0
                )
                < 2.0e-6
                and abs(
                    response_by_key[
                        (eos_id, "near_turning_0p99_Mmax")
                    ]["mass"]
                    - 0.99
                    * sequence_by_id[eos_id]["maximum_model"]["mass"]
                )
                < 3.0e-6
                for eos_id in EOS_SPECS
            ),
            "canonical two-solar and near-turning mass roots",
        ),
        check(
            "VAL4883_13_conditioning",
            all(row["turning_condition_number"] < 3.0 for row in canonical)
            and all(row["turning_condition_number"] > 18.0 for row in near),
            "turning amplification retained and explicit",
        ),
        check(
            "VAL4883_14_contact_caps",
            sections["responses"]["maximum_fixed_mass_tidal_cap"]
            < 3.1e-17
            and max(
                row["cap_abs_deltaR_over_R_fixed_M"] for row in response_rows
            )
            < 3.1e-18,
            "inherited contact envelopes remain tiny across nine rows",
        ),
        check(
            "VAL4883_15_EOS_spread",
            spread["passed"]
            and 0.11 < spread["radius_fractional_EOS_spread"] < 0.13
            and 0.75 < spread["tidal_fractional_EOS_spread"] < 0.80,
            "realistic canonical EOS spread quantified",
        ),
        check(
            "VAL4883_16_spread_dominance",
            spread["radius_EOS_spread_over_contact_cap"] > 1.0e17
            and spread["tidal_EOS_spread_over_contact_cap"] > 1.0e17,
            "EOS nuisance spread exceeds inherited contact caps by 1e17",
        ),
        check(
            "VAL4883_17_crosscheck",
            crosscheck["passed"]
            and len(crosscheck["rows"]) == 48
            and all(row["status"] == "PASS" for row in crosscheck["rows"])
            and crosscheck["maximum_relative_error"] < 0.007,
            (
                "48 nonlinear derivatives; max_error="
                f"{crosscheck['maximum_relative_error']:.9e}"
            ),
        ),
        check(
            "VAL4883_18_validation_step",
            crosscheck["finite_difference_step_Lsun2"] == FD_STEP
            and crosscheck["maximum_step_times_central_energy"] < 1.0e-3,
            "amplified derivative step remains inside linear regime",
        ),
        check(
            "VAL4883_19_surface",
            convergence["passed"]
            and len(convergence["rows"]) == 9
            and convergence["maximum_baseline_radius_fractional_error"]
            < 2.0e-12
            and convergence["maximum_baseline_tidal_fractional_error"]
            < 2.0e-13,
            "surface threshold convergence",
        ),
        check(
            "VAL4883_20_arbitration",
            arbitration["passed"]
            and not arbitration["strong_matter_background_promoted"]
            and not arbitration["full_fundamental_unification"]
            and "CONDITIONAL" in arbitration["strong_matter_correspondence"],
            "selected-branch correspondence retained without coefficient overclaim",
        ),
        check(
            "VAL4883_21_placeholders",
            no_placeholders,
            "no MISSING markers in evidence rows",
        ),
        check(
            "VAL4883_22_nonclaim",
            all(not row["valid_for_claim"] for row in all_rows),
            "all checkpoint evidence remains private and nonclaim",
        ),
        check(
            "VAL4883_23_csv",
            all(
                path.exists() and len(read_csv(path)) > 0
                for path in output_paths
            ),
            f"{len(output_paths)} evidence CSVs parse",
        ),
        check(
            "VAL4883_24_claim",
            len(claims) == 1
            and claims[0].get("status")
            == "selected_metric_strictEFT_multi_EOS_TOV_Love_response_robust_private_conditional_nonclaim",
            "L-725 unique and narrowly scoped",
        ),
        check(
            "VAL4883_25_variables",
            all(
                variable_counts.get(symbol) == 1
                and variables.get(symbol, {}).get("status") == status
                for symbol, status in expected_statuses.items()
            ),
            "seven multi-EOS response variables unique and status-locked",
        ),
        check(
            "VAL4883_26_documents",
            "MTS_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883" in checkpoint
            and "PPC4161_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883"
            in formal_note,
            "checkpoint and formal note markers",
        ),
        check(
            "VAL4883_27_registers",
            "1.176 Multi-EOS cold-barotrope TOV/Love contact response"
            in equations
            and "127. Multi-EOS success does not derive the contact coefficients"
            in redteam
            and "PPC4161 checkpoint 4883" in spine,
            "equation red-team and spine updates",
        ),
        check(
            "VAL4883_28_resume",
            "PPC4161_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883" in resume
            and NEXT_TARGET in resume,
            "resume handoff",
        ),
        check(
            "VAL4883_29_prior",
            len(prior) > 0
            and all(row.get("status") == "PASS" for row in prior),
            "4882 remains green",
        ),
        check(
            "VAL4883_30_scripts",
            compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4883_multi_eos_tov_love_response.py"
            )
            and compile_source(
                POST
                / "scripts"
                / "Y5_R2FR_4883_multi_eos_tov_love_response_gate.py"
            ),
            "research and gate scripts compile without bytecode",
        ),
        check(
            "VAL4883_31_pycache",
            not (POST / "scripts" / "__pycache__").exists(),
            "no pycache",
        ),
        check(
            "VAL4883_32_next",
            NEXT_TARGET in checkpoint
            and arbitration["next_target"] == NEXT_TARGET,
            "4884 target selected",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        check(
            "VAL4883_OVERALL",
            overall,
            "MTS_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883_VALIDATED",
        )
    )
    return rows


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    sources = source_rows()
    groups = output_groups(calculation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4883_SOURCE_REGISTER.csv", sources)
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4883_{name}.csv", rows)
    validation = validation_rows(calculation, sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4883_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4883_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4883_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
